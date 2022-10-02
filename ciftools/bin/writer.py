from typing import Any, List, Optional

import msgpack
import numpy as np
from ciftools.bin.encoder import BYTE_ARRAY, RUN_LENGTH
from ciftools.bin.encoded_data import (
    EncodedCIFCategory,
    EncodedCIFColumn,
    EncodedCIFData,
    EncodedCIFDataBlock,
    EncodedCIFFile,
)
from ciftools.models.writer import CIFWriter, CIFCategoryDesc, CIFCategoryData, CIFFieldDesc


def _always_present(data, i):
    return 0


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

    def write_category(self, category: CIFCategoryDesc, data: List[CIFCategoryData]) -> None:
        if not self._data:
            raise Exception("The writer contents have already been encoded, no more writing.")

        if not self._data_blocks:
            raise Exception("No data block created.")

        filtered_data = list(filter(lambda c: c.count > 0, data))
        if not filtered_data:
            return

        total_count = 0
        for cat in filtered_data:
            total_count += cat.count
        if not total_count:
            return

        encoded: EncodedCIFCategory = {"name": f"_{category.name}", "rowCount": total_count, "columns": []}
        for f in category.fields:
            encoded["columns"].append(_encode_field(f, filtered_data, total_count))

        self._data_blocks[-1]["categories"].append(encoded)

    def encode(self) -> bytes:
        encoded_data = msgpack.dumps(self._data)
        self._data = None
        self._data_blocks = []
        return encoded_data


def _encode_field(field: CIFFieldDesc, data: List[CIFCategoryData], total_count: int) -> EncodedCIFColumn:
    array = field.create_array(total_count)
    is_native: bool = not hasattr(array, "dtype")

    mask = np.zeros(total_count, dtype=np.dtype(np.uint8))
    presence = field.presence or _always_present
    all_present = True

    offset = 0
    for category in data:
        d = category.data

        arrays = field.arrays(d)
        if arrays is not None:
            if len(arrays.values) != category.count:
                raise ValueError(
                    f"values provided in arrays() must have the same length as the category count field"
                )

            array[offset : offset + category.count] = arrays.values

            if arrays.mask is not None:
                if len(arrays.mask) != category.count:
                    raise ValueError(
                        f"mask provided in arrays() must have the same length as the category count field"
                    )
                mask[offset : offset + category.count] = arrays.mask
            offset += category.count

        else:
            # TODO: use numba JIT for this
            for i in range(category.count):
                p = presence(d, i)
                if p:
                    mask[offset] = p
                    if is_native:
                        array[offset] = None
                    all_present = False
                else:
                    array[offset] = field.value(d, i)

                offset += 1

    encoder = field.encoder(data[0].data) if len(data) > 0 else BYTE_ARRAY
    encoded = encoder.encode_cif_data(array)

    mask_data: Optional[EncodedCIFData] = None

    if not all_present:
        mask_rle = RUN_LENGTH.encode(mask)
        if len(mask_rle["data"]) < len(mask):
            mask_data = mask_rle
        else:
            mask_data = BYTE_ARRAY.encode(mask)

    return {"name": field.name, "data": encoded, "mask": mask_data}
