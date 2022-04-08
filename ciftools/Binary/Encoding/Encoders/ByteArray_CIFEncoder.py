import numpy as np

from ciftools.Binary.Encoding.Encoding import ByteArrayEncoding, EEncoding
from ciftools.Binary.Encoding.data_types import DataTypes, EDataTypes
from ciftools.Binary.Encoding.Encoders.ICIFEncoder import ICIFEncoder
from ciftools.Binary.Encoding.EncodedCif.encoded_cif_data import EncodedCIFData


class ByteArray_CIFEncoder(ICIFEncoder):
    @staticmethod
    def __byte_size(data_type: EDataTypes):
        if data_type in (EDataTypes.Int16, EDataTypes.Uint16):
            return 2
        if data_type in (EDataTypes.Int32, EDataTypes.Uint32, EDataTypes.Float32):
            return 4
        return 8

    def encode(self, data: np.ndarray) -> EncodedCIFData:
        data_type: EDataTypes = DataTypes.from_dtype(data.dtype)

        encoding: ByteArrayEncoding = {
            "kind": EEncoding.ByteArray.name,
            "type": data_type
        }
        
        return EncodedCIFData(data=data.tobytes(), encoding=[encoding])
