import unittest

import msgpack
import numpy as np
from ciftools.Binary.decoder import decode_cif_data
from ciftools.Binary.Encoding import binarycif_encoder, encoders


class TestEncodings_StringArray(unittest.TestCase):
    def test(self):
        test_arr = [
            "my",
            "cat",
            "eats",
            "too",
            "much",
            "food",
            "off",
            "my",
            "my",
            "",
            "plate",
            "because",
            "",
            "my",
            "cat",
        ]

        encoder = binarycif_encoder(encoders.STRING_ARRAY_CIF_ENCODER)
        encoded = encoder.encode_cif_data(test_arr)
        msgpack.loads(msgpack.dumps(encoded))
        decoded = decode_cif_data(encoded)

        self.assertTrue(np.array_equal(test_arr, decoded))
