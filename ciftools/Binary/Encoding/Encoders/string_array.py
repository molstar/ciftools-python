import numpy as np
from ciftools.Binary.Encoding import Encoders
from ciftools.Binary.Encoding.EncodedCif.encoded_cif_data import EncodedCIFData
from ciftools.Binary.Encoding.encoder import BinaryCIFEncoder, binarycif_encoder
from ciftools.Binary.Encoding.Encoders.delta import DeltaCIFEncoder
from ciftools.Binary.Encoding.Encoders.base import CIFEncoderBase
from ciftools.Binary.Encoding.Encoders.integer_packing import IntegerPackingCIFEncoder
from ciftools.Binary.Encoding.Encoders.run_length import RunLengthCIFEncoder
from ciftools.Binary.Encoding.Encoding import EncodingEnun, StringArrayEncoding

# TODO: use classifier once implemented
_OFFSET_ENCODER = binarycif_encoder(Encoders.DELTA_CIF_ENCODER, Encoders.INTEGER_PACKING_CIF_ENCODER)
_DATA_ENCODER = binarycif_encoder(Encoders.DELTA_CIF_ENCODER, Encoders.RUN_LENGTH_CIF_ENCODER, Encoders.INTEGER_PACKING_CIF_ENCODER)



class StringArrayCIFEncoder(CIFEncoderBase):
    def encode(self, data: np.ndarray | list[str]) -> EncodedCIFData:
        map = dict()

        strings: list[str] = []
        offsets = [0]
        output = np.empty(len(data), dtype="i4")

        acc_len = 0

        for i, s in enumerate(data):
            # handle null strings.
            if not s:
                output[i] = -1
                continue

            index = map.get(s)
            if index is None:
                # increment the length
                acc_len += len(s)

                # store the string and index
                index = len(strings)
                strings.append(s)
                map[s] = index

                # write the offset
                offsets.append(acc_len)

            output[i] = index

        encoded_offsets = _OFFSET_ENCODER.encode_cif_data(np.array(offsets, dtype="i4"))
        encoded_data = _DATA_ENCODER.encode_cif_data(output)

        encoding: StringArrayEncoding = {
            "dataEncoding": encoded_data["encoding"],
            "kind": EncodingEnun.StringArray,
            "stringData": "".join(strings),
            "offsetEncoding": encoded_offsets["encoding"],
            "offsets": encoded_offsets["data"],
        }

        return EncodedCIFData(data=encoded_data["data"], encoding=[encoding])


STRING_ARRAY_CIF_ENCODER = StringArrayCIFEncoder()