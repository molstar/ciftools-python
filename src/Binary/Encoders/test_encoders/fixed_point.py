import numpy as np

from src.Binary.Decoder import decode_cif_data
from src.Binary.Encoders.FixedPoint_CIFEncoder import FixedPoint_CIFEncoder
from src.Binary.Encoders.RunLength_CIFEncoder import RunLength_CIFEncoder

test_arr = np.random.rand(100) * 100

print(test_arr.dtype.str)

encoder = FixedPoint_CIFEncoder()
encoded = encoder.encode(test_arr, 3, factor=2)

print("TestArr: " + str(test_arr))
print("Encoding: " + str(encoded["encoding"]))
print("EncodedData: " + str(encoded["data"]))

decoded = decode_cif_data(encoded)

print("Decoded: " + str(decoded))