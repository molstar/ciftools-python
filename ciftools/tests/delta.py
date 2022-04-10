import unittest

import msgpack
import numpy as np
from ciftools.binary.decoder import decode_cif_data
from ciftools.binary.encoding import BinaryCIFEncoder, encoders


class TestEncodings_Delta(unittest.TestCase):
    def test(self):
        test_arr = np.array([1, 1, 2, 2, 10, -10])

        encoder = BinaryCIFEncoder(encoders.DELTA_CIF_ENCODER, encoders.BYTE_ARRAY_CIF_ENCODER)
        encoded = encoder.encode_cif_data(test_arr)
        msgpack.loads(msgpack.dumps(encoded))
        decoded = decode_cif_data(encoded)

        self.assertTrue(np.array_equal(test_arr, decoded))
