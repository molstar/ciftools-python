import unittest

import msgpack
import numpy as np
from ciftools.Binary.Decoder import decode_cif_data
from ciftools.Binary.Encoding import binarycif_encoder, encoders


class TestEncodings_RunLength(unittest.TestCase):
    def test(self):

        suite = [np.array([-3] * 9 + [1] * 10 + [2] * 11 + [3] * 12), np.arange(10)]

        for test_arr in suite:
            encoder = binarycif_encoder(encoders.RUN_LENGTH_CIF_ENCODER, encoders.BYTE_ARRAY_CIF_ENCODER)
            encoded = encoder.encode_cif_data(test_arr)
            msgpack.loads(msgpack.dumps(encoded))
            decoded = decode_cif_data(encoded)

            self.assertTrue(np.array_equal(test_arr, decoded))
