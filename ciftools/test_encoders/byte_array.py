import unittest

import numpy as np
from ciftools.Binary.Decoder import decode_cif_data
from ciftools.Binary.Encoders.ByteArray_CIFEncoder import ByteArray_CIFEncoder
from ciftools.Binary.Encoders.INT8_CIFEncoder import INT8_CIFEncoder
from ciftools.Binary.Encoders.UINT8_CIFEncoder import UINT8_CIFEncoder


class TestEncodings_ByteArray(unittest.TestCase):
    def test(self):
        test_arr = np.random.rand(100) * 100
        dep1 = INT8_CIFEncoder()
        dep2 = UINT8_CIFEncoder()
        encoder = ByteArray_CIFEncoder(dep1, dep2)
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
                "ByteArray encoding/decoding pair test failed;\nExpected element '"
                + str(i)
                + "' -> "
                + str(test_arr[i])
                + " but decoded: "
                + str(decoded[i]),
            )
