import unittest

import msgpack
import numpy as np
from ciftools.Binary.Decoder import decode_cif_data
from ciftools.Binary.Encoding.Encoder import BinaryCIFEncoder
from ciftools.Binary.Encoding.Encoders.byte_array import ByteArrayCIFEncoder
from ciftools.Binary.Encoding.Encoders.run_length import RunLengthCIFEncoder


class TestEncodings_RunLength(unittest.TestCase):
    def test(self):

        suite = [np.array([-3] * 9 + [1] * 10 + [2] * 11 + [3] * 12), np.arange(10)]

        for test_arr in suite:
            encoder = BinaryCIFEncoder.by(RunLengthCIFEncoder()).and_(ByteArrayCIFEncoder())
            encoded = encoder.encode_cif_data(test_arr)
            msgpack.loads(msgpack.dumps(encoded))
            decoded = decode_cif_data(encoded)

            self.assertTrue(np.array_equal(test_arr, decoded))
