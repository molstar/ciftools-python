
import numpy as np

from src.Binary.Decoder import decode_cif_data
from src.Binary.Encoders.Delta_CIFEncoder import Delta_CIFEncoder


test_arr = np.random.rand(100) * 100

print(test_arr.dtype.str)

encoder = Delta_CIFEncoder()
encoded = encoder.encode(test_arr)

print("TestArr: " + str(test_arr))
print("Encoding: " + str(encoded["encoding"]))
print("EncodedData: " + str(encoded["data"]))

decoded = decode_cif_data(encoded)

print("Decoded: " + str(decoded))