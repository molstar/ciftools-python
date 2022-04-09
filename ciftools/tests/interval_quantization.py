import unittest

import msgpack
import numpy as np
from ciftools.Binary.Decoder import decode_cif_data
from ciftools.Binary.Encoding.data_types import EDataTypes
from ciftools.Binary.Encoding.Encoder import BinaryCIFEncoder
from ciftools.Binary.Encoding.Encoders.byte_array import ByteArrayCIFEncoder
from ciftools.Binary.Encoding.Encoders.interval_quantization import IntervalQuantizationCIFEncoder


class TestEncodings_IntervalQuantization(unittest.TestCase):
    def test(self):

        test_suite = [
            (np.random.rand(100) * 100, 100, EDataTypes.Uint8),
            (np.random.rand(100) * 100, 2**8 - 1, EDataTypes.Uint8),
            (np.random.rand(100) * 100, 2**16 - 1, EDataTypes.Uint16),
            (np.random.rand(100) * 100, 2**24 - 1, EDataTypes.Uint32),
        ]

        for test_arr, steps, dtype in test_suite:
            low, high = np.min(test_arr), np.max(test_arr)
            encoder = BinaryCIFEncoder.by(IntervalQuantizationCIFEncoder(low, high, steps, dtype)).and_(
                ByteArrayCIFEncoder()
            )
            encoded = encoder.encode_cif_data(test_arr)
            msgpack.loads(msgpack.dumps(encoded))
            decoded = decode_cif_data(encoded)

            self.assertTrue(np.allclose(test_arr, decoded, atol=1.1 * (high - low) / steps))
