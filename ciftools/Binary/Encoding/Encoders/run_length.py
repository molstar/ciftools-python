import numpy as np
from ciftools.Binary.Encoding.data_types import DataTypes, EDataTypes
from ciftools.Binary.Encoding.EncodedCif.encoded_cif_data import EncodedCIFData
from ciftools.Binary.Encoding.Encoders.base import CIFEncoderBase
from ciftools.Binary.Encoding.Encoding import EEncoding, RunLengthEncoding


class RunLengthCIFEncoder(CIFEncoderBase):
    def encode(self, data: np.ndarray) -> EncodedCIFData:
        src_data_type: EDataTypes = DataTypes.from_dtype(data.dtype)

        if not src_data_type:
            data = data.astype(dtype="i4")
            src_data_type = EDataTypes.Int32

        encoding: RunLengthEncoding = {"srcType": src_data_type, "kind": EEncoding.RunLength.name, "srcSize": len(data)}

        if not len(data):
            return EncodedCIFData(data=np.empty(0, dtype="i4"), encoding=[encoding])

        # adapted from https://stackoverflow.com/a/32681075
        y = data[1:] != data[:-1]  # pairwise unequal (string safe)
        pivots = np.append(np.where(y), len(data) - 1)  # must include last element posi
        run_lengths = np.diff(np.append(-1, pivots)).astype("i4")  # run lengths

        encoded_data = np.ravel([data[pivots].astype("i4"), run_lengths], "F")

        return EncodedCIFData(data=encoded_data, encoding=[encoding])


RUN_LENGTH_CIF_ENCODER = RunLengthCIFEncoder()