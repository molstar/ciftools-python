import unittest

import msgpack
import numpy as np
from ciftools.bin.decoder import decode_cif_data
from ciftools.bin.encoder import BYTE_ARRAY, DELTA, ComposeEncoders


class TestEncodings_Delta(unittest.TestCase):
    def test(self):
        test_arr = np.array([1, 1, 2, 2, 10, -10])

        encoder = ComposeEncoders(DELTA, BYTE_ARRAY)

        encoded = encoder.encode(test_arr)
        msgpack.loads(msgpack.dumps(encoded))
        decoded = decode_cif_data(encoded)

        self.assertTrue(np.array_equal(test_arr, decoded))
