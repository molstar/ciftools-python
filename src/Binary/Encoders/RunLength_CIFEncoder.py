import numpy as np
from numpy import int32

from src.Binary.Encoders.ICIFEncoder import ICIFEncoder
from src.Binary.Encoding import RunLengthEncoding
from src.Binary.data_types import DataTypes, EDataTypes
from src.CIFFormat.EncodedCif.encoded_cif_data import EncodedCIFData


class RunLength_CIFEncoder(ICIFEncoder):
    def encode(self, data: np.ndarray, *args, **kwargs) -> EncodedCIFData:
        src_data_type: EDataTypes = DataTypes.from_dtype(data.dtype)

        if not src_data_type:
            data = data.astype(dtype=np.dtype(int32))
            src_data_type = EDataTypes.Int32

        encoding: RunLengthEncoding = RunLengthEncoding()
        encoding.srcType = src_data_type
        encoding.kind = 'RunLength'

        if not len(data):
            encoding.srcSize = 0
            return EncodedCIFData(data=np.empty(0, dtype=np.dtype(int32)), encoding=[encoding])

        full_len = 2
        for i in range (1, len(data)):
            if data[i-1] != data[i]:
                full_len += 2

        encoded_data = np.empty(full_len, dtype=np.dtype(int32))
        offset = 0
        run_len = 1
        for i in range(1, len(data)):
            if data[i-1] != data[i]:
                encoded_data[offset] = data[i-1]
                encoded_data[offset + 1] = run_len
                run_len = 1
                offset += 2
            else:
                run_len = run_len + 1

            encoded_data[offset] = data[-1]
            encoded_data[offset + 1] = run_len

        return EncodedCIFData(data=encoded_data, encoding=[encoding])
