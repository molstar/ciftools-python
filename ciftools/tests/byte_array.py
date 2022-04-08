import unittest

import msgpack
import numpy as np
from ciftools.Binary.Decoder import decode_cif_data
from ciftools.Binary.Encoding.data_types import DataTypes, EDataTypes
from ciftools.Binary.Encoding.Encoder import BinaryCIFEncoder
from ciftools.Binary.Encoding.Encoders.ByteArray_CIFEncoder import ByteArray_CIFEncoder


class TestEncodings_ByteArray(unittest.TestCase):
    def test(self):
        test_suite = [
            (np.array(np.random.rand(100) * 100, dtype="i1"), EDataTypes.Int8),
            (np.array(np.random.rand(100) * 100, dtype="u1"), EDataTypes.Uint8),
            (np.array(np.random.rand(100) * 100, dtype="b"), EDataTypes.Int8),
            (np.array(np.random.rand(100) * 100, dtype="B"), EDataTypes.Uint8),
            (np.array(np.random.rand(100) * 100, dtype="i2"), EDataTypes.Int16),
            (np.array(np.random.rand(100) * 100, dtype="u2"), EDataTypes.Uint16),
            (np.array(np.random.rand(100) * 100, dtype="i4"), EDataTypes.Int32),
            (np.array(np.random.rand(100) * 100, dtype="u4"), EDataTypes.Uint32),
            (np.array(np.random.rand(100) * 100, dtype="f4"), EDataTypes.Float32),
            (np.array(np.random.rand(100) * 100, dtype="f8"), EDataTypes.Float64),
        ]

        for test_arr, expected_type in test_suite:
            encoder = BinaryCIFEncoder.by(ByteArray_CIFEncoder())
            encoded = encoder.encode_cif_data(test_arr)

            msgpack.loads(msgpack.dumps(encoded))

            decoded = decode_cif_data(encoded)

            self.assertTrue(np.array_equal(test_arr, decoded))
            self.assertEqual(encoded["encoding"][0]["type"], expected_type)
