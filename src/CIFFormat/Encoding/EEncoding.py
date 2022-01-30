from enum import Enum


class EEncoding(Enum):
    ByteArray = 0,
    FixedPoint = 1,
    RunLength = 2,
    Delta = 3,
    IntervalQuantization = 4,
    IntegerPacking = 5,
    StringArray = 6
