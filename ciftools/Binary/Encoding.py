from enum import Enum
from typing import TypedDict

import numpy as np


class EEncoding(Enum):
    ByteArray = "ByteArray",
    FixedPoint = "FixedPoint",
    RunLength = "RunLength",
    Delta = "Delta",
    IntervalQuantization = "IntervalQuantization",
    IntegerPacking = "IntegerPacking",
    StringArray = "StringArray"


class EncodingBase(TypedDict):
    kind: str


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
    offsets: np.ndarray
