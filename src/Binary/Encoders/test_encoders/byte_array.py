import numpy as np

from src.Binary.Decoder import decode_cif_data
from src.Binary.Encoders.ByteArray_CIFEncoder import ByteArray_CIFEncoder
from src.Binary.Encoders.INT8_CIFEncoder import INT8_CIFEncoder
from src.Binary.Encoders.UINT8_CIFEncoder import UINT8_CIFEncoder

test_arr = np.random.rand(5) * 100

print(test_arr.dtype.str)

dep1 = INT8_CIFEncoder()
dep2 = UINT8_CIFEncoder()
encoder = ByteArray_CIFEncoder(dep1, dep2)
encoded = encoder.encode(test_arr)

print("TestArr: " + str(test_arr))
print("Encoding: " + str(encoded["encoding"]))
print("EncodedData: " + str(encoded["data"]))

decoded = decode_cif_data(encoded)

print("Decoded: " + str(decoded))