import timeit
import unittest

import msgpack
import numpy as np
from ciftools.binary.decoder import decode_cif_data
from ciftools.binary.encoding import BinaryCIFEncoder
from ciftools.binary.encoding.impl.encoders.byte_array import BYTE_ARRAY_CIF_ENCODER
from ciftools.binary.encoding.impl.encoders.delta import DELTA_CIF_ENCODER


class TestEncodings_Delta(unittest.TestCase):
    def test(self):
        test_arr = np.array([1, 1, 2, 2, 10, -10])

        encoder = BinaryCIFEncoder([DELTA_CIF_ENCODER, BYTE_ARRAY_CIF_ENCODER])

        encoded = encoder.encode_cif_data(test_arr)
        msgpack.loads(msgpack.dumps(encoded))
        decoded = decode_cif_data(encoded)

        self.assertTrue(np.array_equal(test_arr, decoded))
