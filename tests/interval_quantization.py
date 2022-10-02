import unittest

import msgpack
import numpy as np
from ciftools.bin.decoder import decode_cif_data
from ciftools.bin.data_types import DataTypeEnum
from ciftools.bin.encoder import IntervalQuantization, BYTE_ARRAY, ComposeEncoders


class TestEncodings_IntervalQuantization(unittest.TestCase):
    def test(self):

        test_suite = [
            (np.random.rand(100) * 100, 100, DataTypeEnum.Uint8),
            (np.random.rand(100) * 100, 2**8, DataTypeEnum.Uint8),
            (np.array([0, 255], dtype="f4"), 2**8, DataTypeEnum.Uint8),
            (np.random.rand(100) * 100, 2**16, DataTypeEnum.Uint16),
            (np.random.rand(100) * 100, 2**24, DataTypeEnum.Uint32),
        ]

        for test_arr, steps, dtype in test_suite:
            low, high = np.min(test_arr), np.max(test_arr)
            encoder = ComposeEncoders(IntervalQuantization(low, high, steps, dtype), BYTE_ARRAY)
            encoded = encoder.encode(test_arr)
            msgpack.loads(msgpack.dumps(encoded))
            decoded = decode_cif_data(encoded)

            self.assertTrue(np.allclose(test_arr, decoded, atol=1.1 * (high - low) / steps))
