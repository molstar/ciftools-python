import unittest

import msgpack
import numpy as np
from ciftools.Binary.decoder import decode_cif_data
from ciftools.Binary.Encoding import encoders, binarycif_encoder


class TestEncodings_Delta(unittest.TestCase):
    def test(self):
        test_arr = np.array([1, 1, 2, 2, 10, -10])

        encoder = binarycif_encoder(encoders.DELTA_CIF_ENCODER, encoders.BYTE_ARRAY_CIF_ENCODER)
        encoded = encoder.encode_cif_data(test_arr)
        msgpack.loads(msgpack.dumps(encoded))
        decoded = decode_cif_data(encoded)

        self.assertTrue(np.array_equal(test_arr, decoded))
