from numba import jit
from numba.typed import Dict
from numba.core import types
import numpy as np
from ciftools.binary.data_types import DataType
from ciftools.binary.encoded_data import EncodedCIFData
from ciftools.binary.encoding_types import (
    ByteArrayEncoding,
    DeltaEncoding,
    FixedPointEncoding,
    IntegerPackingEncoding,
    IntervalQuantizationEncoding,
    RunLengthEncoding,
    StringArrayEncoding,
)


def decode_cif_data(encoded_data: EncodedCIFData) -> np.ndarray:
    result = encoded_data["data"]
    for encoding in encoded_data["encoding"][::-1]:
        if encoding["kind"] in _decoders:
            result = _decoders[encoding["kind"]](result, encoding)  # type: ignore
        else:
            raise ValueError(f"Unsupported encoding '{encoding['kind']}'")

    return result  # type: ignore


def _decode_byte_array(data: bytes, encoding: ByteArrayEncoding) -> np.ndarray:
    return np.frombuffer(data, dtype=f"<{str(DataType.to_dtype(encoding['type']))}")


def _decode_fixed_point(data: np.ndarray, encoding: FixedPointEncoding) -> np.ndarray:
    return np.array(data, dtype=DataType.to_dtype(encoding["srcType"])) / encoding["factor"]


def _decode_interval_quantization(data: np.ndarray, encoding: IntervalQuantizationEncoding) -> np.ndarray:
    delta = (encoding["max"] - encoding["min"]) / (encoding["numSteps"] - 1)
    return np.array(data, dtype=DataType.to_dtype(encoding["srcType"])) * delta + encoding["min"]


def _decode_run_length(data: np.ndarray, encoding: RunLengthEncoding) -> np.ndarray:
    return np.repeat(np.array(data[::2], dtype=DataType.to_dtype(encoding["srcType"])), repeats=data[1::2])


def _decode_delta(data: np.ndarray, encoding: DeltaEncoding) -> np.ndarray:
    result = np.array(data, dtype=DataType.to_dtype(encoding["srcType"]))
    if encoding["origin"]:
        result[0] += encoding["origin"]
    return np.cumsum(result, out=result)


@jit(nopython=True)
def _decode_integer_packing_signed(data: np.ndarray, encoding_byte_count, encoding_src_size) -> np.ndarray:
    upper_limit = 0x7F if encoding_byte_count == 1 else 0x7FFF
    lower_limit = -upper_limit - 1
    n = len(data)
    output = np.zeros(encoding_src_size, dtype="i4")
    i = 0
    j = 0
    while i < n:
        value = 0
        t = data[i]
        while t == upper_limit or t == lower_limit:
            value += t
            i += 1
            t = data[i]
        value += t
        output[j] = value
        i += 1
        j += 1
    return output


@jit(nopython=True)
def _decode_integer_packing_unsigned(data: np.ndarray, encoding_byte_count, encoding_src_size) -> np.ndarray:
    upper_limit = 0xFF if encoding_byte_count == 1 else 0xFFFF
    n = len(data)
    output = np.zeros(encoding_src_size, dtype="i4")
    i = 0
    j = 0
    print(data)
    while i < n:
        value = 0
        # 255
        t = data[i]
        # yes
        while t == upper_limit:
            # 255
            value += t
            # 1
            i += 1
            # 145
            t = data[i]
        # 255 + 145 = 400
        value += t
        # 400
        output[j] = value
        i += 1
        j += 1
    return output


def _decode_integer_packing(data: np.ndarray, encoding: IntegerPackingEncoding) -> np.ndarray:
    if len(data) == encoding["srcSize"]:
        return data

    # d = dict()
    # for k, v in encoding.items():
    #     d[k] = v

    
    # d1 = Dict.empty(
    #     key_type=types.py2_string_type,
    #     value_type=types.int64,
    # )

    # for k, v in encoding.items():
    #     d1[k] = v

    if encoding["isUnsigned"]:
        return _decode_integer_packing_unsigned(data, encoding["byteCount"], encoding["srcSize"])
    else:
        return _decode_integer_packing_signed(data, encoding["byteCount"], encoding["srcSize"])


def _decode_string_array(data: np.ndarray, encoding: StringArrayEncoding) -> np.ndarray:
    offsets = decode_cif_data(EncodedCIFData(encoding=encoding["offsetEncoding"], data=encoding["offsets"]))
    indices = decode_cif_data(EncodedCIFData(encoding=encoding["dataEncoding"], data=data))

    string_data = encoding["stringData"]
    strings = [""]

    for i in range(1, len(offsets)):
        strings.append(string_data[offsets[i - 1] : offsets[i]])  # type: ignore

    return np.array([strings[i + 1] for i in indices], dtype=np.object_)
    # return [strings[i + 1] for i in indices]


_decoders = {
    "ByteArray": _decode_byte_array,
    "FixedPoint": _decode_fixed_point,
    "IntervalQuantization": _decode_interval_quantization,
    "RunLength": _decode_run_length,
    "Delta": _decode_delta,
    "IntegerPacking": _decode_integer_packing,
    "StringArray": _decode_string_array,
}
