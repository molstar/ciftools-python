import numpy as np
from ciftools.Binary.Encoding.EncodedCif.encoded_cif_data import EncodedCIFData
from ciftools.Binary.Encoding.Encoder import BinaryCIFEncoder
from ciftools.Binary.Encoding.Encoders.Delta_CIFEncoder import Delta_CIFEncoder
from ciftools.Binary.Encoding.Encoders.ICIFEncoder import ICIFEncoder
from ciftools.Binary.Encoding.Encoders.IntegerPacking_CIFEncoder import IntegerPacking_CIFEncoder
from ciftools.Binary.Encoding.Encoders.RunLength_CIFEncoder import RunLength_CIFEncoder
from ciftools.Binary.Encoding.Encoding import EEncoding, StringArrayEncoding


class StringArray_CIFEncoder(ICIFEncoder):
    def __init__(self):
        # TODO: use classifier once implemented
        self.offset_encoder = BinaryCIFEncoder.by(Delta_CIFEncoder()).and_(IntegerPacking_CIFEncoder())
        self.data_encoder = (
            BinaryCIFEncoder.by(Delta_CIFEncoder()).and_(RunLength_CIFEncoder()).and_(IntegerPacking_CIFEncoder())
        )

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

        encoded_offsets = self.offset_encoder.encode_cif_data(np.array(offsets, dtype="i4"))
        encoded_data = self.data_encoder.encode_cif_data(output)

        encoding: StringArrayEncoding = {
            "dataEncoding": encoded_data["encoding"],
            "kind": EEncoding.StringArray.name,
            "stringData": "".join(strings),
            "offsetEncoding": encoded_offsets["encoding"],
            "offsets": encoded_offsets["data"],
        }

        return EncodedCIFData(data=encoded_data["data"], encoding=[encoding])
