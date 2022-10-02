import unittest

import msgpack
import numpy as np
from ciftools.bin.decoder import decode_cif_data
from ciftools.bin.encoder import STRING_ARRAY


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

        encoded = STRING_ARRAY.encode(test_arr)
        msgpack.loads(msgpack.dumps(encoded))
        decoded = decode_cif_data(encoded)

        self.assertTrue(np.array_equal(test_arr, decoded))
