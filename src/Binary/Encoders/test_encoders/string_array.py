import numpy as np

from src.Binary.Decoder import decode_cif_data
from src.Binary.Encoders.ByteArray_CIFEncoder import ByteArray_CIFEncoder
from src.Binary.Encoders.Delta_CIFEncoder import Delta_CIFEncoder
from src.Binary.Encoders.INT8_CIFEncoder import INT8_CIFEncoder
from src.Binary.Encoders.IntegerPacking_CIFEncoder import IntegerPacking_CIFEncoder
from src.Binary.Encoders.RunLength_CIFEncoder import RunLength_CIFEncoder
from src.Binary.Encoders.StringArray_CIFEncoder import StringArray_CIFEncoder
from src.Binary.Encoders.UINT8_CIFEncoder import UINT8_CIFEncoder



test_arr = ["my", "cat", "eats", "too", "much", "food", "off", "my", "plate", "because", "my", "cat"]

encoder1 = Delta_CIFEncoder()

dep1 = INT8_CIFEncoder()
dep2 = UINT8_CIFEncoder()
encoderz = ByteArray_CIFEncoder(dep1, dep2)
encoder2 = IntegerPacking_CIFEncoder(encoderz)

encoder3 = RunLength_CIFEncoder()

encoder = StringArray_CIFEncoder(encoder1, encoder2, encoder3)
encoded = encoder.encode(test_arr)

print("TestArr: " + str(test_arr))
print("Encoding: " + str(encoded["encoding"]))
print("EncodedData: " + str(encoded["data"]))

# not working
decoded = decode_cif_data(encoded)

print("Decoded: " + str(decoded))
