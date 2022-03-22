import math

import numpy as np
from numpy import int32, int8, int16, uint8, uint16

from src.Binary.Encoders.ByteArray_CIFEncoder import ByteArray_CIFEncoder
from src.Binary.Encoders.Delta_CIFEncoder import Delta_CIFEncoder
from src.Binary.Encoders.ICIFEncoder import ICIFEncoder
from src.Binary.Encoders.IntegerPacking_CIFEncoder import IntegerPacking_CIFEncoder
from src.Binary.Encoders.RunLength_CIFEncoder import RunLength_CIFEncoder
from src.Binary.Encoding import IntegerPackingEncoding, StringArrayEncoding, EEncoding
from src.Binary.data_types import DataTypes, EDataTypes
from src.CIFFormat.EncodedCif.encoded_cif_data import EncodedCIFData


class StringArray_CIFEncoder(ICIFEncoder):

    def __init__(self,
                 delta_encoder: Delta_CIFEncoder,
                 integer_packing_encoder: IntegerPacking_CIFEncoder,
                 run_length_encoder: RunLength_CIFEncoder):
        self.delta_encoder = delta_encoder
        self.integer_packing_encoder = integer_packing_encoder
        self.run_length_encoder = run_length_encoder

    def encode(self, data: np.ndarray, *args, **kwargs) -> EncodedCIFData:
        map = dict()
        strings: list(str) = []
        acc_len = 0
        offsets = [0]
        output = []

        i = 0
        for s in data:
            # handle null strings.
            if not s:
                output.append(-1);
                i+=1
                continue

            index = map.get(s, None)
            if index is None:
                # increment the length
                acc_len += len(s)

                # store the string and index
                index = len(strings)
                strings.append(s)
                map[s] = index;

                # write the offset
                offsets.append(acc_len)

            output.append(index)
            i += 1

        # todo: improve api to make this easier -> public api at least
        encoding_offset = self.delta_encoder.encode(np.asarray(offsets))
        encoding_offset2 = self.integer_packing_encoder.encode(encoding_offset["data"])
        encoding_offset["encoding"].extend(encoding_offset2["encoding"])
        encoding_offset["data"] = encoding_offset2["data"]

        encoding_output = self.delta_encoder.encode(np.asarray(output))
        encoding_output2 = self.run_length_encoder.encode(encoding_output["data"])
        encoding_output3 = self.run_length_encoder.encode(encoding_output2["data"])
        encoding_output["encoding"].extend(encoding_offset2["encoding"])
        encoding_output["encoding"].extend(encoding_output3["encoding"])
        encoding_output["data"] = encoding_output3["data"]

        encoding = StringArrayEncoding()
        encoding["kind"] = EEncoding.StringArray
        encoding["dataEncoding"] = encoding_output["encoding"]
        encoding["stringData"] = ''.join(strings)
        encoding["offsetEncoding"] = encoding_offset["encoding"]
        encoding["offsets"] = encoding_offset["data"]

        return EncodedCIFData(data=encoding_output["data"], encoding=[encoding])
