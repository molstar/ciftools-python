import unittest

import numpy as np

from src.Binary.Decoder import decode_cif_data
from src.Binary.Encoders.FixedPoint_CIFEncoder import FixedPoint_CIFEncoder


class TestEncodings_FixedPoint(unittest.TestCase):
    def test(self):
        test_arr = np.random.rand(100) * 100

        print(test_arr.dtype.str)

        encoder = FixedPoint_CIFEncoder()
        encoded = encoder.encode(test_arr, 3, factor=1)

        print("TestArr: " + str(test_arr))
        print("Encoding: " + str(encoded["encoding"]))
        print("EncodedData: " + str(encoded["data"]))

        decoded = decode_cif_data(encoded)

        print("Decoded: " + str(decoded))

        # validate
        for i in range(len(test_arr)):
            self.assertTrue(round(test_arr[i]) == decoded[i],
            "FixedPoint encoding/decoding pair test failed;\nExpected element '"+str(i)+"' -> " + str(test_arr[i]) + " but decoded: "+str(decoded[i]))

