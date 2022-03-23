
from src.Binary.Decoder import decode_cif_data
from src.Binary.Encoders.ByteArray_CIFEncoder import ByteArray_CIFEncoder
from src.Binary.Encoders.Delta_CIFEncoder import Delta_CIFEncoder
from src.Binary.Encoders.INT8_CIFEncoder import INT8_CIFEncoder
from src.Binary.Encoders.IntegerPacking_CIFEncoder import IntegerPacking_CIFEncoder
from src.Binary.Encoders.RunLength_CIFEncoder import RunLength_CIFEncoder
from src.Binary.Encoders.StringArray_CIFEncoder import StringArray_CIFEncoder
from src.Binary.Encoders.UINT8_CIFEncoder import UINT8_CIFEncoder



test_arr = ["my", "cat", "eats", "too", "much", "food", "off", "my", "plate", "because", "my", "cat"]

delta_encoder = Delta_CIFEncoder()

int_encoder = INT8_CIFEncoder()
uint_encoder = UINT8_CIFEncoder()
byte_arr_encoder = ByteArray_CIFEncoder(int_encoder, uint_encoder)
integer_packing_encoder = IntegerPacking_CIFEncoder(byte_arr_encoder)

run_length_encoder = RunLength_CIFEncoder()

encoder = StringArray_CIFEncoder(delta_encoder, integer_packing_encoder, run_length_encoder)
encoded = encoder.encode(test_arr)

print("TestArr: " + str(test_arr))
print("Encoding: " + str(encoded["encoding"]))
print("EncodedData: " + str(encoded["data"]))

# not working
decoded = decode_cif_data(encoded)

print("Decoded: " + str(decoded))
