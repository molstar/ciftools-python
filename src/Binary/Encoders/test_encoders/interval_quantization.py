import numpy as np

from src.Binary.Decoder import decode_cif_data
from src.Binary.Encoders.ByteArray_CIFEncoder import ByteArray_CIFEncoder
from src.Binary.Encoders.INT8_CIFEncoder import INT8_CIFEncoder
from src.Binary.Encoders.IntegerPacking_CIFEncoder import IntegerPacking_CIFEncoder
from src.Binary.Encoders.IntervalQuantization_CIFEncoder import IntervalQuantization_CIFEncoder
from src.Binary.Encoders.UINT8_CIFEncoder import UINT8_CIFEncoder

test_arr = np.random.rand(100) * 100

print(test_arr.dtype.str)

encoder = IntervalQuantization_CIFEncoder()
encoded = encoder.encode(test_arr, 5, min=40, max=60, num_steps=9)

print("TestArr: " + str(test_arr))
print("Encoding: " + str(encoded["encoding"]))
print("EncodedData: " + str(encoded["data"]))

decoded = decode_cif_data(encoded)

print("Decoded: " + str(decoded))