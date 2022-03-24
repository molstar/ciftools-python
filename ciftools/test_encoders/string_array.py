import unittest

from ciftools.Binary.Decoder import decode_cif_data
from ciftools.Binary.Encoders.ByteArray_CIFEncoder import ByteArray_CIFEncoder
from ciftools.Binary.Encoders.Delta_CIFEncoder import Delta_CIFEncoder
from ciftools.Binary.Encoders.INT8_CIFEncoder import INT8_CIFEncoder
from ciftools.Binary.Encoders.IntegerPacking_CIFEncoder import IntegerPacking_CIFEncoder
from ciftools.Binary.Encoders.RunLength_CIFEncoder import RunLength_CIFEncoder
from ciftools.Binary.Encoders.StringArray_CIFEncoder import StringArray_CIFEncoder
from ciftools.Binary.Encoders.UINT8_CIFEncoder import UINT8_CIFEncoder


class TestEncodings_StringArray(unittest.TestCase):
    def test(self):
        test_arr = ["my", "cat", "eats", "too", "much", "food", "off", "my", "plate", "because", "my", "cat"]

        delta_encoder = Delta_CIFEncoder()

        int_encoder = INT8_CIFEncoder()
        uint_encoder = UINT8_CIFEncoder()
        byte_arr_encoder = ByteArray_CIFEncoder(int_encoder, uint_encoder)
        integer_packing_encoder = IntegerPacking_CIFEncoder(byte_arr_encoder)

        run_length_encoder = RunLength_CIFEncoder()

        encoder = StringArray_CIFEncoder(delta_encoder, integer_packing_encoder, run_length_encoder)
        encoded = encoder.encode(test_arr)

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
