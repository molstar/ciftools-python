from typing import Union

import numpy
import numpy as np
from numpy import float64, float32, int32

from src.Binary import Encoding
from src.Binary.Encoders.ICIFEncoder import ICIFEncoder
from src.Binary.Encoding import FixedPointEncoding
from src.CIFFormat.EncodedCif.encoded_cif_data import EncodedCIFData


class FixedPoint_CIFEncoder(ICIFEncoder):

    def encode(self, data: Union[np.ndarray[float64] | np.ndarray[float32]], *args, **kwargs) -> EncodedCIFData:
        if data.dtype is np.dtype(float64):
            src_type = Encoding.DataTypes.Float64
        else:
            src_type = Encoding.DataTypes.Float32

        factor: float = kwargs.get('factor', None)
        if factor is None:
            raise ValueError("FixedPoint encoder factor must be valid")

        processed_data: np.ndarray[int32] = numpy.multiply(data, factor)
        processed_data = processed_data.round()

        encoding: FixedPointEncoding = FixedPointEncoding()
        encoding.kind = 'FixedPoint'
        encoding.factor = factor
        encoding.srcType = src_type
        # TODO: is it needed to call bytes(processed_data)?
        return EncodedCIFData(data=processed_data, encoding=[encoding])
