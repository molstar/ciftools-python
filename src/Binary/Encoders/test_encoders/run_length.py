import numpy as np

from src.Binary.Decoder import decode_cif_data
from src.Binary.Encoders.RunLength_CIFEncoder import RunLength_CIFEncoder

test_arr = np.random.rand(100) * 100

test_arr[0] = 15
test_arr[1] = 15
test_arr[2] = 15
test_arr[3] = 15
test_arr[4] = 15

test_arr[10] = 15
test_arr[11] = 15
test_arr[12] = 15
test_arr[13] = 15
test_arr[14] = 15

print(test_arr.dtype.str)

encoder = RunLength_CIFEncoder()
encoded = encoder.encode(test_arr)

print("TestArr: " + str(test_arr))
print("Encoding: " + str(encoded["encoding"]))
print("EncodedData: " + str(encoded["data"]))

decoded = decode_cif_data(encoded)

print("Decoded: " + str(decoded))