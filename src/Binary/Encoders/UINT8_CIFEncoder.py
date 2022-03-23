import numpy as np
from numpy import uint8

from src.Binary.Encoders.ICIFEncoder import ICIFEncoder
from src.Binary.Encoding import ByteArrayEncoding, EEncoding
from src.Binary.data_types import EDataTypes
from src.CIFFormat.EncodedCif.encoded_cif_data import EncodedCIFData


class UINT8_CIFEncoder(ICIFEncoder):

    def encode(self, data: np.ndarray, *args, **kwargs) -> EncodedCIFData:
        encoding: ByteArrayEncoding = ByteArrayEncoding()
        encoding["kind"] = EEncoding.ByteArray.name
        encoding["type"] = EDataTypes.Uint8
        encoded_data = EncodedCIFData(data=data, encoding=[encoding])
        return encoded_data
