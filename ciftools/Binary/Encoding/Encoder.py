from ciftools.Binary.Encoding.EncodedCif.encoded_cif_data import EncodedCIFData
from ciftools.Binary.Encoding.Encoders.ICIFEncoder import ICIFEncoder
from ciftools.Binary.Encoding.Encoding import EncodingBase


class BinaryCIFEncoder:
    encoders: list[ICIFEncoder]

    def __init__(self, encoders: list[ICIFEncoder]):
        self.encoders: list[ICIFEncoder] = encoders

    def and_(self, f: ICIFEncoder) -> "BinaryCIFEncoder":
        return BinaryCIFEncoder([*self.encoders, f])

    def encode_cif_data(self, data: any) -> EncodedCIFData:
        encodings: list[EncodingBase] = []

        for encoder in self.encoders:
            encoded = encoder.encode(data)
            added_encodings = encoded["encoding"]

            if not added_encodings or not len(added_encodings):
                raise ValueError("Encodings must be non-empty.")

            data = encoded["data"]
            encodings.extend(added_encodings)

        if not isinstance(data, bytes):
            raise ValueError(
                f"The encoding must result in bytes but it was {str(type(data))}. Fix your encoding chain."
            )

        return {"encoding": encodings, "data": data}

    @staticmethod
    def by(f: ICIFEncoder) -> "BinaryCIFEncoder":
        return BinaryCIFEncoder([f])


def binarycif_encoder(*encodings: list[ICIFEncoder]):
    return BinaryCIFEncoder(encodings)
