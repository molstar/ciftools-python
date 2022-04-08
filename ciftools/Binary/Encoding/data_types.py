from __future__ import annotations  # supposed to be in python 3.10 but reverted; maybe in python 3.11?

from enum import IntEnum
from typing import Union

import numpy as np


class EDataTypes(IntEnum):
    Int8 = 1
    Int16 = 2
    Int32 = 3
    Uint8 = 4
    Uint16 = 5
    Uint32 = 6
    Float32 = 32
    Float64 = 33


class DataTypes:
    __data_types_to_dtypes: dict[int, Union[np.dtype, str]] = {
        EDataTypes.Int8.value: "i1",
        EDataTypes.Int16.value: "i2",
        EDataTypes.Int32.value: "i4",
        EDataTypes.Uint8.value: "u1",
        EDataTypes.Uint16.value: "u2",
        EDataTypes.Uint32.value: "u4",
        EDataTypes.Float32.value: "f4",
        EDataTypes.Float64.value: "f8",
    }

    __dtypes_to_data_types: dict[Union[np.dtype, str], int] = {
        **{data_type: dtype for dtype, data_type in __data_types_to_dtypes.items()},
        "b": EDataTypes.Int8.value,
        "B": EDataTypes.Uint8.value,
    }

    @staticmethod
    def from_dtype(dtype: Union[np.dtype, str]) -> EDataTypes:
        return EDataTypes(DataTypes.__dtypes_to_data_types[str(dtype.str).replace("<", "").replace("|", "")])

    @staticmethod
    def to_dtype(data_type: Union[EDataTypes, int]) -> Union[np.dtype, str]:
        return DataTypes.__data_types_to_dtypes[int(data_type)]
