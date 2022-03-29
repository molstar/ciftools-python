import unittest

from ciftools.Binary.Decoder import decode_cif_data
from ciftools.Binary.Encoding.Encoder import BinaryCIFEncoder
from ciftools.Binary.Encoding.Encoders.ByteArray_CIFEncoder import ByteArray_CIFEncoder
from ciftools.Binary.Encoding.Encoders import StringArray_CIFEncoder


class TestEncodings_StringArray(unittest.TestCase):
    def test(self):
        test_arr = ["my", "cat", "eats", "too", "much", "food", "off", "my", "plate", "because", "my", "cat"]

        encoder = BinaryCIFEncoder.by(StringArray_CIFEncoder()).and_(ByteArray_CIFEncoder())
        encoded = encoder.encode_cif_data(test_arr)

        print("TestArr: " + str(test_arr))
        print("Encoding: " + str(encoded["encoding"]))
        print("EncodedData: " + str(encoded["data"]))

        decoded = decode_cif_data(encoded)

        print("Decoded: " + str(decoded))

        # validate
        for i in range(len(test_arr)):
            self.assertTrue(
                test_arr[i] == decoded[i],
                "StringArray encoding/decoding pair test failed;\nExpected element '"
                + str(i)
                + "' -> "
                + str(test_arr[i])
                + " but decoded: "
                + str(decoded[i]),
            )
