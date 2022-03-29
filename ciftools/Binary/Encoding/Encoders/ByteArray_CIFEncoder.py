import numpy as np
from ciftools.Binary.data_types import DataTypes, EDataTypes
from ciftools.Binary.Encoding.Encoders.ICIFEncoder import ICIFEncoder
from ciftools.Binary.Encoding.Encoders.INT8_CIFEncoder import INT8_CIFEncoder
from ciftools.Binary.Encoding.Encoders.UINT8_CIFEncoder import UINT8_CIFEncoder
from ciftools.Binary.Encoding import ByteArrayEncoding, EEncoding
from ciftools.CIFFormat.EncodedCif.encoded_cif_data import EncodedCIFData


class ByteArray_CIFEncoder(ICIFEncoder):
    def __init__(self):
        self._int8_encoder = INT8_CIFEncoder()
        self._uint8_encoder = UINT8_CIFEncoder()

    @staticmethod
    def __byte_size(data_type: EDataTypes):
        if data_type in (EDataTypes.Int16, EDataTypes.Uint16):
            return 2
        if data_type in (EDataTypes.Int32, EDataTypes.Uint32, EDataTypes.Float32):
            return 4
        return 8

    def encode(self, data: np.ndarray) -> EncodedCIFData:
        data_type: EDataTypes = DataTypes.from_dtype(data.dtype)

        if data_type == EDataTypes.Int8:
            return self._int8_encoder.encode(data)
        elif data_type == EDataTypes.Uint8:
            return self._uint8_encoder.encode(data)

        encoding: ByteArrayEncoding = {
            "kind": EEncoding.ByteArray.name,
            "type": data_type
        }
        # TODO: improve typing of conversion from ndarray to bytes back to nd array
        return EncodedCIFData(data=data.tobytes(), encoding=[encoding])
