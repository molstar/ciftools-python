from typing import Any
from ciftools.binary.encoding.base.cif_encoder_base import CIFEncoderBase
from ciftools.binary.encoding.encodings import EncodingBase
from ciftools.binary.encoding.types import EncodedCIFData


class BinaryCIFEncoder:
    def __init__(self, encoders: list[CIFEncoderBase]):
        self.encoders: list[CIFEncoderBase] = encoders

    def encode_cif_data(self, data: Any) -> EncodedCIFData:
        encodings: list[EncodingBase] = []

        for encoder in self.encoders:
            # get EncodedCIFData typeddict with 'data' and 'encoding'
            encoded = encoder.encode(data)
            # get ref to 'encoding' of that typeddict
            added_encodings = encoded["encoding"]

            # if 'encoding' is None or 0 - raise Error
            if not added_encodings or not len(added_encodings):
                raise ValueError("Encodings must be non-empty.")

            # get ref to 'data' of typeddict
            data = encoded["data"]

            # add 'encoding' to list of encodings
            encodings.extend(added_encodings)

            # on next iteration, already encoded data by the first encoder,
            # is encoded by the 2nd, then by 3rd, each time encoding is added to list

        if not isinstance(data, bytes):
            raise ValueError(
                f"The encoding must result in bytes but it was {str(type(data))}. Fix your encoding chain."
            )

        return {"encoding": encodings, "data": data}
