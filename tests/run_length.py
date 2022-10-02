import unittest

import msgpack
import numpy as np
from ciftools.bin.decoder import decode_cif_data
from ciftools.bin.encoder import RUN_LENGTH, BYTE_ARRAY, Compose



class TestEncodings_RunLength(unittest.TestCase):
    def test(self):

        suite = [np.array([-3] * 9 + [1] * 10 + [2] * 11 + [3] * 12), np.arange(10)]

        for test_arr in suite:
            encoder = Compose(RUN_LENGTH, BYTE_ARRAY)
            encoded = encoder.encode(test_arr)
            msgpack.loads(msgpack.dumps(encoded))
            decoded = decode_cif_data(encoded)

            self.assertTrue(np.array_equal(test_arr, decoded))
