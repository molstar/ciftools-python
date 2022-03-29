import numpy as np
from ciftools.Binary.Encoding.data_types import DataTypes, EDataTypes
from ciftools.Binary.Encoding.Encoders.ICIFEncoder import ICIFEncoder
from ciftools.Binary.Encoding import EEncoding, RunLengthEncoding
from ciftools.Binary.Encoding.EncodedCif.encoded_cif_data import EncodedCIFData
from numpy import int32


class RunLength_CIFEncoder(ICIFEncoder):
    def encode(self, data: np.ndarray) -> EncodedCIFData:
        src_data_type: EDataTypes = DataTypes.from_dtype(data.dtype)

        if not src_data_type:
            data = data.astype(dtype=np.dtype(int32))
            src_data_type = EDataTypes.Int32

        encoding: RunLengthEncoding = {
            "srcType": src_data_type,
            "kind": EEncoding.RunLength.name
        }

        if not len(data):
            encoding.srcSize = 0
            return EncodedCIFData(data=np.empty(0, dtype=np.dtype(int32)), encoding=[encoding])

        full_len = 2
        for i in range(1, len(data)):
            if data[i - 1] != data[i]:
                full_len += 2

        encoded_data = np.empty(full_len, dtype=np.dtype(int32))
        offset = 0
        run_len = 1
        for i in range(1, len(data)):
            if data[i - 1] != data[i]:
                encoded_data[offset] = data[i - 1]
                encoded_data[offset + 1] = run_len
                run_len = 1
                offset += 2
            else:
                run_len = run_len + 1

            encoded_data[offset] = data[-1]
            encoded_data[offset + 1] = run_len

        return EncodedCIFData(data=encoded_data, encoding=[encoding])
