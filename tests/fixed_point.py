import unittest

import msgpack
import numpy as np
from ciftools.bin.decoder import decode_cif_data
from ciftools.bin.encoder import BYTE_ARRAY, DELTA, FixedPoint, Compose


class TestEncodings_FixedPoint(unittest.TestCase):
    def test(self):

        test_suite = [
            (np.random.rand(100) * 1000, 1),
            (np.random.rand(100) * 1000, 2),
            (np.random.rand(100) * 1000, 3),
            (np.random.rand(100) * 1000, 4),
        ]

        for test_arr, e in test_suite:
            encoder = Compose(FixedPoint(10**e), BYTE_ARRAY)
            encoded = encoder.encode(test_arr)
            decoded = decode_cif_data(encoded)

            self.assertTrue(np.allclose(test_arr, decoded, atol=10 ** (-e)))


class TestEncodings_FixedPointDelta(unittest.TestCase):
    def test(self):

        test_suite = [
            (np.random.rand(100) * 1000, 1),
            (np.random.rand(100) * 1000, 2),
            (np.random.rand(100) * 1000, 3),
            (np.random.rand(100) * 1000, 4),
            (np.array([24.41149862, 93.41400854, 25.07853073, 86.43384453, 73.12187345], dtype="f4"), 3),
        ]

        for test_arr, e in test_suite:
            encoder = Compose(FixedPoint(10**e), DELTA, BYTE_ARRAY)
            encoded = encoder.encode(test_arr)
            msgpack.loads(msgpack.dumps(encoded))
            decoded = decode_cif_data(encoded)

            self.assertTrue(np.allclose(test_arr, decoded, atol=10 ** (-e)))
