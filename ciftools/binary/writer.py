from typing import Any, List, Optional
from numba import jit
import msgpack
import numpy as np
from ciftools.binary.encoded_data import (
    EncodedCIFCategory,
    EncodedCIFColumn,
    EncodedCIFData,
    EncodedCIFDataBlock,
    EncodedCIFFile,
)
from ciftools.binary.encoder import BYTE_ARRAY, RUN_LENGTH
from ciftools.models.writer import CIFCategoryDesc, CIFFieldDesc, CIFWriter


def _always_present(data, i):
    return 0


class _DataWrapper:
    data: Any
    count: int

    def __init__(self, data: Any, count: int):
        self.data = data
        self.count = count


class BinaryCIFWriter(CIFWriter):
    _data: Optional[EncodedCIFFile]
    _data_blocks: list[EncodedCIFDataBlock]
    _encoded_data: np.ndarray  # bytes -> uint8

    def __init__(self, encoder: str):
        self._data_blocks = []
        self._data = {"version": "0.3.0", "encoder": encoder, "dataBlocks": self._data_blocks}

    def start_data_block(self, header: str) -> None:
        # TODO: should we call upper() here?
        _header = header.replace(" ", "").replace("\n", "").replace("\t", "").upper()
        self._data_blocks.append({"header": _header, "categories": []})

    def write_category(self, category: CIFCategoryDesc, data: List[Any]) -> None:
        if not self._data:
            raise Exception("The writer contents have already been encoded, no more writing.")

        if not self._data_blocks:
            raise Exception("No data block created.")

        instances = [_DataWrapper(data=d, count=category.get_row_count(d)) for d in data]
        instances = list(filter(lambda i: i.count > 0, instances))
        if not instances:
            return

        total_count = 0
        for cat in instances:
            total_count += cat.count
        if not total_count:
            return

        fields = category.get_field_descriptors(instances[0].data)
        encoded: EncodedCIFCategory = {"name": f"_{category.name}", "rowCount": total_count, "columns": []}
        for f in fields:
            encoded["columns"].append(_encode_field(f, instances, total_count))

        self._data_blocks[-1]["categories"].append(encoded)

    def write_category_not_optimized(self, category: CIFCategoryDesc, data: List[Any]) -> None:
        if not self._data:
            raise Exception("The writer contents have already been encoded, no more writing.")

        if not self._data_blocks:
            raise Exception("No data block created.")

        instances = [_DataWrapper(data=d, count=category.get_row_count(d)) for d in data]
        instances = list(filter(lambda i: i.count > 0, instances))
        if not instances:
            return

        total_count = 0
        for cat in instances:
            total_count += cat.count
        if not total_count:
            return

        fields = category.get_field_descriptors(instances[0].data)
        encoded: EncodedCIFCategory = {"name": f"_{category.name}", "rowCount": total_count, "columns": []}
        for f in fields:
            encoded["columns"].append(_encode_field_not_optimized(f, instances, total_count))

        self._data_blocks[-1]["categories"].append(encoded)

    def encode(self) -> bytes:
        encoded_data = msgpack.dumps(self._data)
        self._data = None
        self._data_blocks = []
        return encoded_data

def _first_loop(presence, mask, category, array, field, d, offset):
    for i in range(category.count):
        p = presence(d, i)
        if p:
            mask[offset] = p
            all_present = False
        else:
            array[offset] = field.value(d, i)  # type: ignore
        offset += 1


    return array, all_present, mask, offset

@jit(forceobj=True)
def _second_loop(category, array, offset, field, d):
    for i in range(category.count):
        array[offset] = field.value(d, i)  # type: ignore
        offset += 1

    return array, offset

def _encode_field(field: CIFFieldDesc, data: List[_DataWrapper], total_count: int) -> EncodedCIFColumn:
    array = field.create_array(total_count)

    mask = np.zeros(total_count, dtype=np.dtype(np.uint8))
    presence = field.presence
    all_present = True

    offset = 0
    for category in data:
        d = category.data

        category_array = field.value_array and field.value_array(d)
        if category_array is not None:
            if len(category_array) != category.count:
                raise ValueError(f"provided values array must have the same length as the category count field")

            array[offset : offset + category.count] = category_array  # type: ignore

            category_mask = field.presence_array and field.presence_array(d)
            if category_mask is not None:
                if len(category_mask) != category.count:
                    raise ValueError(f"provided mask array must have the same length as the category count field")
                mask[offset : offset + category.count] = category_mask

            offset += category.count

        elif presence is not None:
            # TODO: check if JIT will help
            for i in range(category.count):
                p = presence(d, i)
                if p:
                    mask[offset] = p
                    all_present = False
                else:
                    array[offset] = field.value(d, i)  # type: ignore
                offset += 1
        else:
            # TODO: check if JIT will help
            array, offset = _second_loop(category, array, offset, field, d)

    encoder = field.encoder(data[0].data) if len(data) > 0 else BYTE_ARRAY
    encoded = encoder.encode(array)

    if not isinstance(encoded["data"], bytes):
        raise ValueError(
            f"The encoding must result in bytes but it was {str(type(encoded['data']))}. Fix the encoding chain."
        )

    mask_data: Optional[EncodedCIFData] = None

    if not all_present:
        mask_rle = RUN_LENGTH.encode(mask)
        if len(mask_rle["data"]) < len(mask):
            mask_data = mask_rle
        else:
            mask_data = BYTE_ARRAY.encode(mask)

    return {"name": field.name, "data": encoded, "mask": mask_data}

def _encode_field_not_optimized(field: CIFFieldDesc, data: List[_DataWrapper], total_count: int) -> EncodedCIFColumn:
    array = field.create_array(total_count)

    mask = np.zeros(total_count, dtype=np.dtype(np.uint8))
    presence = field.presence
    all_present = True

    offset = 0
    for category in data:
        d = category.data

        category_array = field.value_array and field.value_array(d)
        if category_array is not None:
            if len(category_array) != category.count:
                raise ValueError(f"provided values array must have the same length as the category count field")

            array[offset : offset + category.count] = category_array  # type: ignore

            category_mask = field.presence_array and field.presence_array(d)
            if category_mask is not None:
                if len(category_mask) != category.count:
                    raise ValueError(f"provided mask array must have the same length as the category count field")
                mask[offset : offset + category.count] = category_mask

            offset += category.count

        elif presence is not None:
            # TODO: check if JIT will help
            for i in range(category.count):
                p = presence(d, i)
                if p:
                    mask[offset] = p
                    all_present = False
                else:
                    array[offset] = field.value(d, i)  # type: ignore
                offset += 1
        else:
            # TODO: check if JIT will help
            for i in range(category.count):
                array[offset] = field.value(d, i)  # type: ignore
                offset += 1

    encoder = field.encoder(data[0].data) if len(data) > 0 else BYTE_ARRAY
    encoded = encoder.encode(array)

    if not isinstance(encoded["data"], bytes):
        raise ValueError(
            f"The encoding must result in bytes but it was {str(type(encoded['data']))}. Fix the encoding chain."
        )

    mask_data: Optional[EncodedCIFData] = None

    if not all_present:
        mask_rle = RUN_LENGTH.encode(mask)
        if len(mask_rle["data"]) < len(mask):
            mask_data = mask_rle
        else:
            mask_data = BYTE_ARRAY.encode(mask)

    return {"name": field.name, "data": encoded, "mask": mask_data}