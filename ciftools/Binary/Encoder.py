# TODO: refactor with new code format

from typing import Union

import numpy as np
from numpy import uint8, int8, int16, int32

from ciftools.Binary import Encoding
from ciftools.Binary.Encoders.FixedPoint_CIFEncoder import FixedPoint_CIFEncoder
from ciftools.Binary.Encoders.ICIFEncoder import ICIFEncoder
from ciftools.Binary.Encoding import DataTypes, ByteArrayEncoding, FixedPointEncoding, IntervalQuantizationEncoding, \
    RunLengthEncoding, DeltaEncoding, IntegerPackingEncoding, StringArrayEncoding, EEncoding, EncodingBase
from ciftools.CIFFormat.EncodedCif.encoded_cif_data import EncodedCIFData


# "IntervalQuantization": _decode_interval_quantization,
# "RunLength": _decode_run_length,
# "Delta": _decode_delta,
# "IntegerPacking": _decode_integer_packing,
# "StringArray": _decode_string_array,
# "ByteArray": _decode_byte_array,

_encoders: dict[str, ICIFEncoder] = {
    "FixedPoint": FixedPoint_CIFEncoder(),
}


def encode_cif_data(data: object) -> EncodedCIFData:
    encodings: EncodingBase = []

    for encoding, encoder in _encoders.items():
        encoded = encoder.encode(data);
        added_encodings = encoded.get["encoding"]

        if not added_encodings or not len(added_encodings):
            raise ValueError('Encodings must be non-empty.')

        data = encoded["data"]
        for added_encoding in added_encodings:
            encodings["encoding"].push(added_encoding);

    if not isinstance(data, list(uint8)):
        raise ValueError('The encoding must result in a list(uint8) but it was ' + type(data) +'. Fix your encoding chain.');

    encoded_data = EncodedCIFData()
    encoded_data["encoding"] = encodings
    encoded_data["data"] = data
    return encoded_data



