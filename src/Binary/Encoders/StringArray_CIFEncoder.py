import math

import numpy as np
from numpy import int32, int8, int16, uint8, uint16

from src.Binary.Encoders.ByteArray_CIFEncoder import ByteArray_CIFEncoder
from src.Binary.Encoders.ICIFEncoder import ICIFEncoder
from src.Binary.Encoding import IntegerPackingEncoding
from src.Binary.data_types import DataTypes, EDataTypes
from src.CIFFormat.EncodedCif.encoded_cif_data import EncodedCIFData


class StringArray_CIFEncoder(ICIFEncoder):
    def encode(self, data: np.ndarray, *args, **kwargs) -> EncodedCIFData:
        pass
