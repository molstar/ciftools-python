import unittest

import numpy as np
import msgpack
from ciftools.Binary.Decoder import decode_cif_data
from ciftools.Binary.Encoding.Encoder import BinaryCIFEncoder
from ciftools.Binary.Encoding.Encoders.Delta_CIFEncoder import Delta_CIFEncoder
from ciftools.Binary.Encoding.Encoders.FixedPoint_CIFEncoder import FixedPoint_CIFEncoder
from ciftools.Binary.Encoding.Encoders.ByteArray_CIFEncoder import ByteArray_CIFEncoder


class TestEncodings_FixedPoint(unittest.TestCase):
    def test(self):

        test_suite = [
            (np.random.rand(100) * 1000, 1),
            (np.random.rand(100) * 1000, 2),
            (np.random.rand(100) * 1000, 3),
            (np.random.rand(100) * 1000, 4),
        ]

        for test_arr, e in test_suite:
            encoder = BinaryCIFEncoder.by(FixedPoint_CIFEncoder(10 ** e)).and_(ByteArray_CIFEncoder())
            encoded = encoder.encode_cif_data(test_arr)
            decoded = decode_cif_data(encoded)

            self.assertTrue(np.allclose(test_arr, decoded, atol=10 ** (-e)))


class TestEncodings_FixedPointDelta(unittest.TestCase):
    def test(self):

        test_suite = [
            (np.random.rand(100) * 1000, 1),
            (np.random.rand(100) * 1000, 2),
            (np.random.rand(100) * 1000, 3),
            (np.random.rand(100) * 1000, 4),
            (np.array([24.41149862, 93.41400854, 25.07853073, 86.43384453, 73.12187345], dtype='f4'), 3)
        ]

        for test_arr, e in test_suite:
            encoder = BinaryCIFEncoder.by(FixedPoint_CIFEncoder(10 ** e)).and_(Delta_CIFEncoder()).and_(ByteArray_CIFEncoder())
            encoded = encoder.encode_cif_data(test_arr)
            msgpack.loads(msgpack.dumps(encoded))
            decoded = decode_cif_data(encoded)

            self.assertTrue(np.allclose(test_arr, decoded, atol=10 ** (-e)))
