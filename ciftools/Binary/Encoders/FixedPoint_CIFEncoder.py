from typing import Union

import numpy
import numpy as np
from ciftools.Binary.data_types import EDataTypes
from ciftools.Binary.Encoders.ICIFEncoder import ICIFEncoder
from ciftools.Binary.Encoding import EEncoding, FixedPointEncoding
from ciftools.CIFFormat.EncodedCif.encoded_cif_data import EncodedCIFData
from numpy import float64, int32


class FixedPoint_CIFEncoder(ICIFEncoder):
    def __init__(self, factor: float):
        self._factor = factor

    def encode(self, data: np.ndarray, *args, **kwargs) -> EncodedCIFData:
        if data.dtype is np.dtype(float64):
            src_type = EDataTypes.Float64
        else:
            src_type = EDataTypes.Float32

        if self._factor is None:
            raise ValueError("FixedPoint encoder factor must be valid")

        processed_data: np.ndarray[int32] = numpy.multiply(data, self._factor)
        processed_data = processed_data.round()

        encoding: FixedPointEncoding = {
            "kind": EEncoding.FixedPoint.name,
            "srcType": src_type,
            "factor": self._factor
        }

        # TODO: is it needed to call bytes(processed_data)?
        return EncodedCIFData(data=processed_data, encoding=[encoding])
