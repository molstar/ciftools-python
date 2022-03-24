import unittest

import numpy as np
from ciftools.Binary.Decoder import decode_cif_data
from ciftools.Binary.Encoders.RunLength_CIFEncoder import RunLength_CIFEncoder


class TestEncodings_RunLength(unittest.TestCase):
    def test(self):
        test_arr = np.random.randint(0, 100, 100)

        test_arr[0] = 15
        test_arr[1] = 15
        test_arr[2] = 15
        test_arr[3] = 15
        test_arr[4] = 15
        test_arr[5] = 15
        test_arr[6] = 15
        test_arr[7] = 15
        test_arr[8] = 15

        test_arr[10] = 17
        test_arr[11] = 17
        test_arr[12] = 17

        test_arr[13] = 16
        test_arr[14] = 16

        encoder = RunLength_CIFEncoder()
        encoded = encoder.encode(test_arr)

        print("TestArr: " + str(test_arr))
        print("Encoding: " + str(encoded["encoding"]))
        print("EncodedData: " + str(encoded["data"]))

        decoded = decode_cif_data(encoded)

        print("Decoded: " + str(decoded))

        # validate
        for i in range(len(test_arr)):
            self.assertTrue(
                int(test_arr[i]) == round(decoded[i]),
                "RunLength encoding/decoding pair test failed;\nExpected element '"
                + str(i)
                + "' -> "
                + str(test_arr[i])
                + " but decoded: "
                + str(decoded[i]),
            )
