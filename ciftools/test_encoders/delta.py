import unittest

import numpy as np

from ciftools.Binary.Decoder import decode_cif_data
from ciftools.Binary.Encoders.Delta_CIFEncoder import Delta_CIFEncoder


class TestEncodings_Delta(unittest.TestCase):
    def test(self):
        test_arr = np.random.randint(0, 100, 100)

        encoder = Delta_CIFEncoder()
        encoded = encoder.encode(test_arr)

        print("TestArr: " + str(test_arr))
        print("Encoding: " + str(encoded["encoding"]))
        print("EncodedData: " + str(encoded["data"]))

        decoded = decode_cif_data(encoded)

        print("Decoded: " + str(decoded))

        # validate
        for i in range(len(test_arr)):
            self.assertTrue(test_arr[i] == decoded[i],
                            "Delta encoding/decoding pair test failed;\nExpected element '" + str(i) + "' -> " + str(
                                test_arr[i]) + " but decoded: " + str(decoded[i]))