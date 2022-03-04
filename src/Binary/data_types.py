from __future__ import annotations  # supposed to be in python 3.10 but reverted; maybe in python 3.11?

from enum import Enum
from typing import Union

import numpy as np


class EDataTypes(Enum):
    Int8 = 1
    Int16 = 2
    Int32 = 3
    Uint8 = 4
    Uint16 = 5
    Uint32 = 6
    Float32 = 32
    Float64 = 33


class DataTypes:
    __data_types_to_dtypes: dict[DataTypes, Union[np.dtype, str]] = {
        EDataTypes.Int8: "i1",
        EDataTypes.Int16: "i2",
        EDataTypes.Int32: "i4",
        EDataTypes.Uint8: "u1",
        EDataTypes.Uint16: "u2",
        EDataTypes.Uint32: "u4",
        EDataTypes.Float32: "f4",
        EDataTypes.Float64: "f8",
    }

    __dtypes_to_data_types: dict[Union[np.dtype, str], EDataTypes] = \
        {dtype: data_type for (dtype, data_type) in __data_types_to_dtypes}

    @staticmethod
    def from_dtype(dtype: Union[np.dtype, str]) -> EDataTypes:
        return DataTypes.__dtypes_to_data_types[dtype]

    @staticmethod
    def to_dtype(data_type: EDataTypes) -> Union[np.dtype, str]:
        return DataTypes.__data_types_to_dtypes[data_type]
