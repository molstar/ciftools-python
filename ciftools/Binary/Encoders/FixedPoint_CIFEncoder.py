from typing import Union

import numpy
import numpy as np
from ciftools.Binary import Encoding
from ciftools.Binary.data_types import EDataTypes
from ciftools.Binary.Encoders.ICIFEncoder import ICIFEncoder
from ciftools.Binary.Encoding import EEncoding, FixedPointEncoding
from ciftools.CIFFormat.EncodedCif.encoded_cif_data import EncodedCIFData
from numpy import float32, float64, int32


class FixedPoint_CIFEncoder(ICIFEncoder):
    def encode(self, data: np.ndarray, *args, **kwargs) -> EncodedCIFData:
        if data.dtype is np.dtype(float64):
            src_type = EDataTypes.Float64
        else:
            src_type = EDataTypes.Float32

        factor: float = kwargs.get("factor", None)
        if factor is None:
            raise ValueError("FixedPoint encoder factor must be valid")

        processed_data: np.ndarray[int32] = numpy.multiply(data, factor)
        processed_data = processed_data.round()

        encoding: FixedPointEncoding = FixedPointEncoding()
        encoding["kind"] = EEncoding.FixedPoint.name
        encoding["factor"] = factor
        encoding["srcType"] = src_type
        # TODO: is it needed to call bytes(processed_data)?
        return EncodedCIFData(data=processed_data, encoding=[encoding])
