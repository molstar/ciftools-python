import unittest

import numpy as np
from ciftools.Binary.Decoder import decode_cif_data
from ciftools.Binary.Encoding.Encoder import BinaryCIFEncoder
from ciftools.Binary.Encoding.Encoders.ByteArray_CIFEncoder import ByteArray_CIFEncoder
from ciftools.Binary.Encoding.Encoders.RunLength_CIFEncoder import RunLength_CIFEncoder


class TestEncodings_RunLength(unittest.TestCase):
    def test(self):
        test_arr = np.array([1] * 10 + [2] * 11 + [3] * 12)

        encoder = BinaryCIFEncoder.by(RunLength_CIFEncoder()).and_(ByteArray_CIFEncoder())
        encoded = encoder.encode_cif_data(test_arr)
        decoded = decode_cif_data(encoded)

        self.assertEqual(list(test_arr), list(decoded))
