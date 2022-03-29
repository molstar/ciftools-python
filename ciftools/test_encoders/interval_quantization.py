import unittest

import numpy as np
from ciftools.Binary.Decoder import decode_cif_data
from ciftools.Binary.Encoding.Encoder import BinaryCIFEncoder
from ciftools.Binary.Encoding.Encoders.ByteArray_CIFEncoder import ByteArray_CIFEncoder
from ciftools.Binary.Encoding.Encoders.IntervalQuantization_CIFEncoder import IntervalQuantization_CIFEncoder


class TestEncodings_IntervalQuantization(unittest.TestCase):
    def test(self):
        test_arr = np.random.rand(100) * 100

        encoder = BinaryCIFEncoder.by(IntervalQuantization_CIFEncoder(0, 100, 10000)).and_(ByteArray_CIFEncoder())
        encoded = encoder.encode_cif_data(test_arr)

        print("TestArr: " + str(test_arr))
        print("Encoding: " + str(encoded["encoding"]))
        print("EncodedData: " + str(encoded["data"]))

        decoded = decode_cif_data(encoded)

        print("Decoded: " + str(decoded))

        # validate
        for i in range(len(test_arr)):
            self.assertTrue(
                test_arr[i] - decoded[i] < 0.1,
                "IntervalQuantization encoding/decoding pair test failed;\nExpected element '"
                + str(i)
                + "' -> "
                + str(test_arr[i])
                + " but decoded: "
                + str(decoded[i]),
            )
