import math

import numpy as np
from ciftools.Binary.data_types import DataTypes, EDataTypes
from ciftools.Binary.Encoders.ByteArray_CIFEncoder import ByteArray_CIFEncoder
from ciftools.Binary.Encoders.Delta_CIFEncoder import Delta_CIFEncoder
from ciftools.Binary.Encoders.ICIFEncoder import ICIFEncoder
from ciftools.Binary.Encoders.IntegerPacking_CIFEncoder import IntegerPacking_CIFEncoder
from ciftools.Binary.Encoders.RunLength_CIFEncoder import RunLength_CIFEncoder
from ciftools.Binary.Encoding import EEncoding, IntegerPackingEncoding, StringArrayEncoding
from ciftools.CIFFormat.EncodedCif.encoded_cif_data import EncodedCIFData
from numpy import int8, int16, int32, uint8, uint16


class StringArray_CIFEncoder(ICIFEncoder):
    def __init__(
        self,
        delta_encoder: Delta_CIFEncoder,
        integer_packing_encoder: IntegerPacking_CIFEncoder,
        run_length_encoder: RunLength_CIFEncoder,
    ):
        self.delta_encoder = delta_encoder
        self.integer_packing_encoder = integer_packing_encoder
        self.run_length_encoder = run_length_encoder

    def encode(self, data: np.ndarray, *args, **kwargs) -> EncodedCIFData:
        map = dict()
        strings: list(str) = []
        acc_len = 0
        offsets = []
        output = []

        for s in data:
            # handle null strings.
            if not s:
                output.append(-1)
                continue

            index = map.get(s, None)
            if index is None:
                # increment the length
                acc_len += len(s)

                # store the string and index
                index = len(strings)
                strings.append(s)
                map[s] = index

                # write the offset
                offsets.append(acc_len)

            output.append(index)

        # todo: improve api to make this easier -> public api at least
        encoding_offset = self.delta_encoder.encode(np.asarray(offsets))
        encoding_offset2 = self.integer_packing_encoder.encode(encoding_offset["data"])
        encoding_offset["encoding"].extend(encoding_offset2["encoding"])
        encoding_offset["data"] = encoding_offset2["data"]

        encoding_output = self.delta_encoder.encode(np.asarray(output))
        encoding_output2 = self.run_length_encoder.encode(encoding_output["data"])
        encoding_output3 = self.integer_packing_encoder.encode(encoding_output2["data"])
        encoding_output["encoding"].extend(encoding_output2["encoding"])
        encoding_output["encoding"].extend(encoding_output3["encoding"])
        encoding_output["data"] = encoding_output3["data"]

        encoding = StringArrayEncoding()
        encoding["kind"] = EEncoding.StringArray.name
        encoding["dataEncoding"] = encoding_output["encoding"]
        encoding["stringData"] = "".join(strings)
        encoding["offsetEncoding"] = encoding_offset["encoding"]
        encoding["offsets"] = encoding_offset["data"]

        return EncodedCIFData(data=encoding_output["data"], encoding=[encoding])
