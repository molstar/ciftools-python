import numpy
import numpy as np
from ciftools.Binary.Encoding.data_types import EDataTypes
from ciftools.Binary.Encoding.EncodedCif.encoded_cif_data import EncodedCIFData
from ciftools.Binary.Encoding.Encoders.base import CIFEncoderBase
from ciftools.Binary.Encoding.Encoding import EEncoding, FixedPointEncoding
from numpy import float64, int32


class FixedPointCIFEncoder(CIFEncoderBase):
    def __init__(self, factor: float):
        self._factor = factor

    def encode(self, data: np.ndarray, *args, **kwargs) -> EncodedCIFData:
        if data.dtype is np.dtype(float64):
            src_type = EDataTypes.Float64
        else:
            src_type = EDataTypes.Float32

        if self._factor is None:
            raise ValueError("FixedPoint encoder factor must be valid")

        fixed_point_data: np.ndarray[int32] = np.array(data * self._factor, dtype="i4")

        encoding: FixedPointEncoding = {"kind": EEncoding.FixedPoint.name, "srcType": src_type, "factor": self._factor}

        return EncodedCIFData(data=fixed_point_data, encoding=[encoding])
