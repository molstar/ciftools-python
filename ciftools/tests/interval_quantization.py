import unittest

import msgpack
import numpy as np
from ciftools.binary.decoder import decode_cif_data
from ciftools.binary.encoding import BinaryCIFEncoder, encoders
from ciftools.binary.encoding.data_types import DataTypeEnum


class TestEncodings_IntervalQuantization(unittest.TestCase):
    def test(self):

        test_suite = [
            (np.random.rand(100) * 100, 100, DataTypeEnum.Uint8),
            (np.random.rand(100) * 100, 2**8 - 1, DataTypeEnum.Uint8),
            (np.random.rand(100) * 100, 2**16 - 1, DataTypeEnum.Uint16),
            (np.random.rand(100) * 100, 2**24 - 1, DataTypeEnum.Uint32),
        ]

        for test_arr, steps, dtype in test_suite:
            low, high = np.min(test_arr), np.max(test_arr)
            encoder = BinaryCIFEncoder(
                encoders.IntervalQuantizationCIFEncoder(low, high, steps, dtype), encoders.BYTE_ARRAY_CIF_ENCODER
            )
            encoded = encoder.encode_cif_data(test_arr)
            msgpack.loads(msgpack.dumps(encoded))
            decoded = decode_cif_data(encoded)

            self.assertTrue(np.allclose(test_arr, decoded, atol=1.1 * (high - low) / steps))
