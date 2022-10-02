import math
import sys
from typing import Any, List, Protocol, Union

import numpy as np
from ciftools.binary.data_types import DataType, DataTypeEnum
from ciftools.binary.encoded_data import EncodedCIFData
from ciftools.binary.encoding_types import (
    ByteArrayEncoding,
    DeltaEncoding,
    EncodingEnun,
    FixedPointEncoding,
    IntegerPackingEncoding,
    IntervalQuantizationEncoding,
    RunLengthEncoding,
    StringArrayEncoding,
)


class BinaryCIFEncoder(Protocol):
    def encode(self, data: Any) -> EncodedCIFData:
        ...

class ComposeEncoders(BinaryCIFEncoder):
    def __init__(self, *encoders: List["BinaryCIFEncoder"]):
        self.encoders = encoders

    def encode(self, data: Any) -> EncodedCIFData:
        encodings: List[Any] = []

        for encoder in self.encoders:
            encoded = encoder.encode(data)
            added_encodings = encoded["encoding"]

            if not added_encodings or not len(added_encodings):
                raise ValueError("Encodings must be non-empty.")

            data = encoded["data"]
            encodings.extend(added_encodings)

        if not isinstance(data, bytes):
            raise ValueError(f"The encoding must result in bytes but it was {str(type(data))}. Fix the encoding chain.")

        return {"encoding": encodings, "data": data}


class ByteArray(BinaryCIFEncoder):
    def encode(self, data: np.ndarray) -> EncodedCIFData:
        data_type: DataTypeEnum = DataType.from_dtype(data.dtype)

        encoding: ByteArrayEncoding = {"kind": EncodingEnun.ByteArray, "type": data_type}

        bo = data.dtype.byteorder
        if bo == ">" or (bo == "=" and sys.byteorder == "big"):
            new_bo = data.dtype.newbyteorder("<")
            data = np.array(data, dtype=new_bo)

        return EncodedCIFData(data=data.tobytes(), encoding=[encoding])

BYTE_ARRAY = ByteArray()

class Delta(BinaryCIFEncoder):
    def encode(self, data: np.ndarray) -> EncodedCIFData:
        src_data_type: DataTypeEnum = DataType.from_dtype(data.dtype)

        if not src_data_type or src_data_type not in (DataTypeEnum.Int8, DataTypeEnum.Int16, DataTypeEnum.Int32):
            data = data.astype(dtype="i4")
            src_data_type = DataTypeEnum.Int32

        encoding: DeltaEncoding = {"kind": EncodingEnun.Delta, "srcType": src_data_type}

        data_length = len(data)

        if not data_length:
            encoding.origin = 0
            return EncodedCIFData(data=np.empty(0, dtype="i4"), encoding=[encoding])

        encoded_data = np.diff(data, prepend=data[0])
        encoding["origin"] = int(data[0])

        return EncodedCIFData(data=encoded_data, encoding=[encoding])

DELTA = Delta()

class FixedPoint(BinaryCIFEncoder):
    def __init__(self, factor: float):
        self._factor = factor

    def encode(self, data: np.ndarray, *args, **kwargs) -> EncodedCIFData:
        if data.dtype is np.dtype(np.float64):
            src_type = DataTypeEnum.Float64
        else:
            src_type = DataTypeEnum.Float32

        if self._factor is None:
            raise ValueError("FixedPoint encoder factor must be valid")

        fixed_point_data: np.ndarray = np.array(data * self._factor, dtype="i4")

        encoding: FixedPointEncoding = {"kind": EncodingEnun.FixedPoint, "srcType": src_type, "factor": self._factor}

        return EncodedCIFData(data=fixed_point_data, encoding=[encoding])


class IntegerPacking(BinaryCIFEncoder):
    def encode(self, data: np.ndarray) -> EncodedCIFData:

        # TODO: must be 32bit integer

        packing = _determine_packing(data)
        if packing.bytesPerElement == 4:
            return BYTE_ARRAY.encode(data)

        # integer packing

        if packing.isSigned:
            if packing.bytesPerElement == 1:
                upper_limit = 0x7F
                packed = np.empty(packing.size, dtype=np.int8)
            else:
                upper_limit = 0x7FFF
                packed = np.empty(packing.size, dtype=np.int16)
        else:
            if packing.bytesPerElement == 1:
                upper_limit = 0xFF
                packed = np.empty(packing.size, dtype=np.uint8)
            else:
                upper_limit = 0xFFFF
                packed = np.empty(packing.size, dtype=np.uint16)

        lower_limit = -upper_limit - 1

        # TODO: figure out if there is a way to implement this
        # better & faster with numpy methods.
        _pack_values(data, upper_limit, lower_limit, packed)

        byte_array_result = BYTE_ARRAY.encode(packed)

        integer_packing_encoding: IntegerPackingEncoding = {
            "kind": EncodingEnun.IntegerPacking,
            "isUnsigned": not packing.isSigned,
            "srcSize": len(data),
            "byteCount": packing.bytesPerElement,
        }

        return EncodedCIFData(
            data=byte_array_result["data"], encoding=[integer_packing_encoding, byte_array_result["encoding"][0]]
        )


class _PackingInfo:
    isSigned: bool
    size: int
    bytesPerElement: int


def _pack_values(data: np.ndarray, upper_limit: int, lower_limit: int, target: np.ndarray) -> None:
    offset = 0
    for value in data:
        if value >= 0:
            while value >= upper_limit:
                target[offset] = upper_limit
                offset += 1
                value -= upper_limit
        else:
            while value <= lower_limit:
                target[offset] = lower_limit
                offset += 1
                value -= lower_limit

        target[offset] = value
        offset += 1


def _determine_packing(data: np.ndarray) -> _PackingInfo:
    # determine sign
    is_signed = np.any(data < 0)

    # determine packing size
    size8 = _packing_size_signed(data, 0x7F) if is_signed else _packing_size_unsigned(data, 0xFF)
    size16 = _packing_size_signed(data, 0x7FFF) if is_signed else _packing_size_unsigned(data, 0xFFFF)

    packing = _PackingInfo()
    packing.isSigned = is_signed

    data_len = len(data)

    if data_len * 4 < size16 * 2:
        packing.size = data_len
        packing.bytesPerElement = 4

    elif size16 * 2 < size8:
        packing.size = size16
        packing.bytesPerElement = 2

    else:
        packing.size = size8
        packing.bytesPerElement = 1

    return packing


def _packing_size_signed(data: np.ndarray, upper_limit: int) -> int:
    lower_limit = -upper_limit - 1
    size = 0

    for value in data:
        if value >= 0:
            size += math.floor(value / upper_limit)
        else:
            size += math.floor(value / lower_limit)

    return size + len(data)


def _packing_size_unsigned(data: np.ndarray, upper_limit: int) -> int:
    size = 0

    for value in data:
        size += math.floor(value / upper_limit)

    return size + len(data)


INTEGER_PACKING = IntegerPacking()


class IntervalQuantization(BinaryCIFEncoder):
    def __init__(self, minimum: int, maximum: int, num_steps: int, array_type: DataTypeEnum = DataTypeEnum.Uint32):
        self._min = minimum
        self._max = maximum
        self._num_steps = num_steps
        self._array_type = array_type

    def encode(self, data: np.ndarray, *args, **kwargs) -> EncodedCIFData:
        src_data_type: DataTypeEnum = DataType.from_dtype(data.dtype)

        # TODO: determine min/max from data if not set?
        if self._max < self._min:
            t = self._min
            self._min = self._max
            self._max = t

        encoding: IntervalQuantizationEncoding = {
            "min": float(self._min),
            "max": float(self._max),
            "numSteps": self._num_steps,
            "srcType": src_data_type,
            "kind": EncodingEnun.IntervalQuantization,
        }

        dtype = DataType.to_dtype(self._array_type)

        if not len(data):
            return EncodedCIFData(data=np.empty(0, dtype=dtype), encoding=[encoding])

        delta = (self._max - self._min) / (self._num_steps - 1)

        quantized = np.clip(data, self._min, self._max)
        np.subtract(quantized, self._min, out=quantized)
        np.divide(quantized, delta, out=quantized)
        np.round(quantized, 0, out=quantized)

        encoded_data = np.array(quantized, dtype=dtype)

        return EncodedCIFData(data=encoded_data, encoding=[encoding])


class RunLength(BinaryCIFEncoder):
    def encode(self, data: np.ndarray) -> EncodedCIFData:
        src_data_type: DataTypeEnum = DataType.from_dtype(data.dtype)

        if not src_data_type:
            data = data.astype(dtype="i4")
            src_data_type = DataTypeEnum.Int32

        encoding: RunLengthEncoding = {"srcType": src_data_type, "kind": EncodingEnun.RunLength, "srcSize": len(data)}

        if not len(data):
            return EncodedCIFData(data=np.empty(0, dtype="i4"), encoding=[encoding])

        # adapted from https://stackoverflow.com/a/32681075
        y = data[1:] != data[:-1]  # pairwise unequal (string safe)
        pivots = np.append(np.where(y), len(data) - 1)  # must include last element posi
        run_lengths = np.diff(np.append(-1, pivots)).astype("<i4")  # run lengths

        encoded_data = np.ravel([data[pivots].astype("<i4"), run_lengths], "F")

        return EncodedCIFData(data=encoded_data, encoding=[encoding])


RUN_LENGTH = RunLength()


# TODO: use classifier once implemented
_OFFSET_ENCODER = ComposeEncoders(DELTA, INTEGER_PACKING)
_DATA_ENCODER = ComposeEncoders(DELTA, RUN_LENGTH, INTEGER_PACKING)


class StringArray(BinaryCIFEncoder):
    def encode(self, data: Union[np.ndarray, list[str]]) -> EncodedCIFData:
        _map = dict()

        strings: list[str] = []
        offsets = [0]
        indices = np.empty(len(data), dtype="<i4")

        acc_len = 0

        for i, s in enumerate(data):
            # handle null strings.
            if not s:
                indices[i] = -1
                continue

            index = _map.get(s)
            if index is None:
                # increment the length
                acc_len += len(s)

                # store the string and index
                index = len(strings)
                strings.append(s)
                _map[s] = index

                # write the offset
                offsets.append(acc_len)

            indices[i] = index

        encoded_offsets = _OFFSET_ENCODER.encode(np.array(offsets, dtype="<i4"))
        encoded_data = _DATA_ENCODER.encode(indices)

        encoding: StringArrayEncoding = {
            "dataEncoding": encoded_data["encoding"],
            "kind": EncodingEnun.StringArray,
            "stringData": "".join(strings),
            "offsetEncoding": encoded_offsets["encoding"],
            "offsets": encoded_offsets["data"],
        }

        return EncodedCIFData(data=encoded_data["data"], encoding=[encoding])

STRING_ARRAY = StringArray()
