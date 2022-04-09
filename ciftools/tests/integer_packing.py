import unittest

import msgpack
import numpy as np
from ciftools.Binary.Decoder import decode_cif_data
from ciftools.Binary.Encoding.Encoder import BinaryCIFEncoder
from ciftools.Binary.Encoding.Encoders.integer_packing import IntegerPackingCIFEncoder


class TestEncodings_IntegerPackingSigned(unittest.TestCase):
    def test(self):
        test_suite = [
            (np.array([0, 1]), True, 1),
            (np.array([-1, 1]), False, 1),
            (np.array([0, 1000, 14000]), True, 2),
            (np.array([-1000, 1000, 14000, -14000]), False, 2),
        ]

        for test_arr, is_unsigned, byte_count in test_suite:
            encoder = BinaryCIFEncoder.by(IntegerPackingCIFEncoder())
            encoded = encoder.encode_cif_data(test_arr)
            decoded = decode_cif_data(encoded)
            msgpack.loads(msgpack.dumps(encoded))

            self.assertTrue(np.array_equal(test_arr, decoded))
            self.assertEqual(is_unsigned, encoded["encoding"][0]["isUnsigned"])
            self.assertEqual(byte_count, encoded["encoding"][0]["byteCount"])
