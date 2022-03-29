# TODO: refactor with new code format

from ciftools.Binary.Encoding.Encoders.ICIFEncoder import ICIFEncoder
from ciftools.Binary.Encoding import (
    EncodingBase,
)
from ciftools.Binary.Encoding.EncodedCif.encoded_cif_data import EncodedCIFData

from ciftools.Binary.Encoding.data_types import DataTypes, EDataTypes


class BinaryCIFEncoder:
    encoders: list[ICIFEncoder]

    def __init__(self, encoders: list[ICIFEncoder]):
        self.encoders: list[ICIFEncoder] = encoders

    def and_(self, f: ICIFEncoder):
        encoders = list(self.encoders)
        encoders.append(f)
        return BinaryCIFEncoder(encoders)

    def encode_cif_data(self, data: any) -> EncodedCIFData:
        encodings: list[EncodingBase] = []

        for encoder in self.encoders:
            encoded = encoder.encode(data)
            added_encodings = encoded["encoding"]

            if not added_encodings or not len(added_encodings):
                raise ValueError('Encodings must be non-empty.')

            data = encoded["data"]
            encodings.extend(added_encodings)

        if not (isinstance(data, bytes) or (DataTypes.from_dtype(data.dtype) is EDataTypes.Uint8)):
            raise ValueError('The encoding must result in a nparray of (uint8) but it was ' + str(type(data)) + ' ' + str(data.dtype) + ' . Fix your encoding chain.');

        return {"encoding": encodings, "data": data }

    @staticmethod
    def by(f: ICIFEncoder):
        return BinaryCIFEncoder([f])
