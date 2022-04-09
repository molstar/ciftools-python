import numpy as np
import sys
from ciftools.Binary.Encoding.data_types import DataType, DataTypeEnum
from ciftools.Binary.Encoding.EncodedCif.encoded_cif_data import EncodedCIFData
from ciftools.Binary.Encoding.Encoders.base import CIFEncoderBase
from ciftools.Binary.Encoding.Encoding import ByteArrayEncoding, EncodingEnun


class ByteArrayCIFEncoder(CIFEncoderBase):
    @staticmethod
    def __byte_size(data_type: DataTypeEnum):
        if data_type in (DataTypeEnum.Int16, DataTypeEnum.Uint16):
            return 2
        if data_type in (DataTypeEnum.Int32, DataTypeEnum.Uint32, DataTypeEnum.Float32):
            return 4
        return 8

    def encode(self, data: np.ndarray) -> EncodedCIFData:
        data_type: DataTypeEnum = DataType.from_dtype(data.dtype)

        encoding: ByteArrayEncoding = {"kind": EncodingEnun.ByteArray, "type": data_type}

        bo = data.dtype.byteorder
        if bo == ">" or (bo == "=" and sys.byteorder == "big"):
            new_bo = data.dtype.newbyteorder("<")
            data = np.array(data, dtype=new_bo)

        # TODO: ensure little endian
        return EncodedCIFData(data=data.tobytes(), encoding=[encoding])


BYTE_ARRAY_CIF_ENCODER = ByteArrayCIFEncoder()