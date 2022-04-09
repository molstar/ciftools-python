import unittest

import msgpack
import numpy as np
from ciftools.Binary.decoder import decode_cif_data
from ciftools.Binary.Encoding import encoders, binarycif_encoder


class TestEncodings_IntegerPackingSigned(unittest.TestCase):
    def test(self):
        test_suite = [
            (np.array([0, 1]), True, 1),
            (np.array([-1, 1]), False, 1),
            (np.array([0, 1000, 14000]), True, 2),
            (np.array([-1000, 1000, 14000, -14000]), False, 2),
        ]

        for test_arr, is_unsigned, byte_count in test_suite:
            encoder = binarycif_encoder(encoders.INTEGER_PACKING_CIF_ENCODER)
            encoded = encoder.encode_cif_data(test_arr)
            decoded = decode_cif_data(encoded)
            msgpack.loads(msgpack.dumps(encoded))

            self.assertTrue(np.array_equal(test_arr, decoded))
            self.assertEqual(is_unsigned, encoded["encoding"][0]["isUnsigned"])
            self.assertEqual(byte_count, encoded["encoding"][0]["byteCount"])
