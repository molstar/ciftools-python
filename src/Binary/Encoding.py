from enum import Enum


class DataTypes(Enum):
    Int8 = 1
    Int16 = 2
    Int32 = 3
    Uint8 = 4
    Uint16 = 5
    Uint32 = 6
    Float32 = 32
    Float64 = 33


class EEncoding(Enum):
    ByteArray = 0,
    FixedPoint = 1,
    RunLength = 2,
    Delta = 3,
    IntervalQuantization = 4,
    IntegerPacking = 5,
    StringArray = 6


class EncodingBase:
    kind: EEncoding


class ByteArrayEncoding(EncodingBase):
    type: int


class FixedPointEncoding(EncodingBase):
    factor: float
    srcType: int


class IntervalQuantizationEncoding(EncodingBase):
    min: float
    max: float
    numSteps: int
    srcType: int


class RunLengthEncoding(EncodingBase):
    srcType: int
    srcSize: int


class DeltaEncoding(EncodingBase):
    origin: int
    srcType: int


class IntegerPackingEncoding(EncodingBase):
    byteCount: int
    isUnsigned: bool
    srcSize: int


class StringArrayEncoding(EncodingBase):
    dataEncoding: list[EncodingBase]
    stringData: str
    offsetEncoding: list[EncodingBase]
    offsets: bytes
