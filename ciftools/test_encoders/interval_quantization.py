import unittest

import numpy as np
from ciftools.Binary.Decoder import decode_cif_data
from ciftools.Binary.Encoding.Encoder import BinaryCIFEncoder
from ciftools.Binary.Encoding.Encoders.ByteArray_CIFEncoder import ByteArray_CIFEncoder
from ciftools.Binary.Encoding.Encoders.IntervalQuantization_CIFEncoder import IntervalQuantization_CIFEncoder


class TestEncodings_IntervalQuantization(unittest.TestCase):
    def test(self):

        test_suite = [
            (np.random.rand(100) * 100, 100),
            (np.random.rand(100) * 100, 2**8 - 1),
            (np.random.rand(100) * 100, 2**16 - 1),
        ]

        for test_arr, steps in test_suite:
            low, high = np.min(test_arr), np.max(test_arr)
            encoder = BinaryCIFEncoder.by(IntervalQuantization_CIFEncoder(low, high, steps)).and_(ByteArray_CIFEncoder())
            encoded = encoder.encode_cif_data(test_arr)
            decoded = decode_cif_data(encoded)

            self.assertTrue(np.allclose(test_arr, decoded, atol=1.1 * (high - low) / steps))
