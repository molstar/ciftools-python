import unittest

import numpy as np
from ciftools.Binary.Decoder import decode_cif_data
from ciftools.Binary.Encoding.Encoder import BinaryCIFEncoder
from ciftools.Binary.Encoding.Encoders.FixedPoint_CIFEncoder import FixedPoint_CIFEncoder
from ciftools.Binary.Encoding.Encoders.ByteArray_CIFEncoder import ByteArray_CIFEncoder


class TestEncodings_FixedPoint(unittest.TestCase):
    def test(self):

        test_suite = [
            (np.random.rand(100) * 100, 1),
            (np.random.rand(100) * 100, 2),
            (np.random.rand(100) * 100, 3),
            (np.random.rand(100) * 100, 4),
        ]

        for test_arr, e in test_suite:
            encoder = BinaryCIFEncoder.by(FixedPoint_CIFEncoder(10 ** e)).and_(ByteArray_CIFEncoder())
            encoded = encoder.encode_cif_data(test_arr)
            decoded = decode_cif_data(encoded)

            self.assertTrue(np.allclose(test_arr, decoded, atol=10 ** (-e)))
