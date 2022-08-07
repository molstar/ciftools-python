import unittest

import msgpack
import numpy as np
from ciftools.binary.decoder import decode_cif_data
from ciftools.binary.encoding import BinaryCIFEncoder
from ciftools.src.binary.encoding.impl import BYTE_ARRAY_CIF_ENCODER
from ciftools.src.binary.encoding.impl import RUN_LENGTH_CIF_ENCODER


class TestEncodings_RunLength(unittest.TestCase):
    def test(self):

        suite = [np.array([-3] * 9 + [1] * 10 + [2] * 11 + [3] * 12), np.arange(10)]

        for test_arr in suite:
            encoder = BinaryCIFEncoder([RUN_LENGTH_CIF_ENCODER, BYTE_ARRAY_CIF_ENCODER])
            encoded = encoder.encode_cif_data(test_arr)
            msgpack.loads(msgpack.dumps(encoded))
            decoded = decode_cif_data(encoded)

            self.assertTrue(np.array_equal(test_arr, decoded))
