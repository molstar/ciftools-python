import numpy as np

from src.Binary.Encoders.INT8_CIFEncoder import INT8_CIFEncoder
from src.Binary.Encoders.ICIFEncoder import ICIFEncoder
from src.Binary.Encoders.UINT8_CIFEncoder import UINT8_CIFEncoder
from src.Binary.Encoding import ByteArrayEncoding
from src.Binary.data_types import DataTypes, EDataTypes
from src.CIFFormat.EncodedCif.encoded_cif_data import EncodedCIFData


class ByteArray_CIFEncoder(ICIFEncoder):
    def __init__(self, int8_encoder: INT8_CIFEncoder, uint8_encoder: UINT8_CIFEncoder):
        self.int8_encoder = int8_encoder
        self.uint8_encoder = uint8_encoder

    @staticmethod
    def __byte_size (data_type: EDataTypes):
        if data_type in (EDataTypes.Int16, EDataTypes.Uint16):
            return 2
        if data_type in (EDataTypes.Int32, EDataTypes.Uint32, EDataTypes.Float32):
            return 4
        return 8

    def encode(self, data: np.ndarray, *args, **kwargs) -> EncodedCIFData:
        data_type: EDataTypes = DataTypes.from_dtype(data.dtype)

        if data_type == EDataTypes.Int8:
            return self.int8_encoder.encode(data)
        elif data_type == EDataTypes.Uint8:
            return self.uint8_encoder.encode(data)

        byte_size = ByteArray_CIFEncoder.__byte_size(data_type)
        encoded_data = np.empty(len(data) * byte_size)
        data_bytes = data.tobytes()

        for i in range(len(data)):
            encoded_data.put(
                [byte_size*i + x for x in range(byte_size)],
                [data_bytes[y] for y in range(byte_size*i, byte_size*i + byte_size)],
                mode='raise')

        encoding = ByteArrayEncoding()
        encoding.kind = 'ByteArray'
        encoding.type = data_type
        return EncodedCIFData(data=encoded_data, encoding=[encoding])
