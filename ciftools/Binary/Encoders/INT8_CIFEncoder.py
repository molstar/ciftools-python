import numpy as np
from ciftools.Binary.data_types import EDataTypes
from ciftools.Binary.Encoders.ICIFEncoder import ICIFEncoder
from ciftools.Binary.Encoding import ByteArrayEncoding, EEncoding
from ciftools.CIFFormat.EncodedCif.encoded_cif_data import EncodedCIFData
from numpy import uint8


class INT8_CIFEncoder(ICIFEncoder):
    def encode(self, data: np.ndarray) -> EncodedCIFData:
        encoding: ByteArrayEncoding = {
            "kind": EEncoding.ByteArray.name,
            "type": EDataTypes.Int8,
        }
        # TODO: is it needed to call uint8(data)?
        encoded_data = EncodedCIFData(data=uint8(data), encoding=[encoding])
        return encoded_data
