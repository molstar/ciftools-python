import numpy as np

from ciftools.Binary.Encoding.Encoding import EEncoding, DeltaEncoding
from ciftools.Binary.Encoding.data_types import DataTypes, EDataTypes
from ciftools.Binary.Encoding.Encoders.ICIFEncoder import ICIFEncoder
from ciftools.Binary.Encoding.EncodedCif.encoded_cif_data import EncodedCIFData
from numpy import int32


class Delta_CIFEncoder(ICIFEncoder):
    def encode(self, data: np.ndarray) -> EncodedCIFData:

        # TODO: must be signed integer

        src_data_type: EDataTypes = DataTypes.from_dtype(data.dtype)

        if not src_data_type:
            data = data.astype(dtype=np.dtype(int32))
            src_data_type = EDataTypes.Int32

        encoding: DeltaEncoding = {
            "kind": EEncoding.Delta.name,
            "srcType": src_data_type
        }

        data_length = len(data)

        if not data_length:
            encoding.origin = 0
            return EncodedCIFData(data=np.empty(0, dtype=np.dtype(int32)), encoding=[encoding])

        encoded_data = np.empty(data_length, dtype=np.dtype(int32))

        origin_data = data[0]
        encoded_data[0] = origin_data

        for i in range(1, data_length):
            encoded_data[i] = data[i] - data[i - 1]

        encoded_data[0] = 0
        encoding["origin"] = origin_data
        return EncodedCIFData(data=encoded_data, encoding=[encoding])
