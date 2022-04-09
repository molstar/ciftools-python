import numpy as np
from ciftools.binary.encoding.data_types import DataTypeEnum
from ciftools.binary.encoding.encoders.base import CIFEncoderBase
from ciftools.binary.encoding.encodings import EncodingEnun, FixedPointEncoding
from numpy import float64

from ciftools.binary.encoding.types import EncodedCIFData


class FixedPointCIFEncoder(CIFEncoderBase):
    def __init__(self, factor: float):
        self._factor = factor

    def encode(self, data: np.ndarray, *args, **kwargs) -> EncodedCIFData:
        if data.dtype is np.dtype(float64):
            src_type = DataTypeEnum.Float64
        else:
            src_type = DataTypeEnum.Float32

        if self._factor is None:
            raise ValueError("FixedPoint encoder factor must be valid")

        fixed_point_data: np.ndarray = np.array(data * self._factor, dtype="i4")

        encoding: FixedPointEncoding = {"kind": EncodingEnun.FixedPoint, "srcType": src_type, "factor": self._factor}

        return EncodedCIFData(data=fixed_point_data, encoding=[encoding])
