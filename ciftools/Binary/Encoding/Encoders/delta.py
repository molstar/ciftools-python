import numpy as np
from ciftools.Binary.Encoding.data_types import DataTypes, EDataTypes
from ciftools.Binary.Encoding.EncodedCif.encoded_cif_data import EncodedCIFData
from ciftools.Binary.Encoding.Encoders.base import CIFEncoderBase
from ciftools.Binary.Encoding.Encoding import DeltaEncoding, EEncoding
from numpy import int32


class DeltaCIFEncoder(CIFEncoderBase):
    def encode(self, data: np.ndarray) -> EncodedCIFData:
        src_data_type: EDataTypes = DataTypes.from_dtype(data.dtype)

        if not src_data_type or src_data_type not in (EDataTypes.Int8, EDataTypes.Int16, EDataTypes.Int32):
            data = data.astype(dtype=np.dtype(int32))
            src_data_type = EDataTypes.Int32

        encoding: DeltaEncoding = {"kind": EEncoding.Delta.name, "srcType": src_data_type}

        data_length = len(data)

        if not data_length:
            encoding.origin = 0
            return EncodedCIFData(data=np.empty(0, dtype=np.dtype(int32)), encoding=[encoding])

        encoded_data = np.diff(data, prepend=data[0])
        encoding["origin"] = int(data[0])

        return EncodedCIFData(data=encoded_data, encoding=[encoding])


DELTA_CIF_ENCODER = DeltaCIFEncoder()