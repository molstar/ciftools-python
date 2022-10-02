from argparse import ArgumentError
import pytest
import msgpack
import numpy as np
from ciftools.binary.encoding.data_types import DataTypeEnum
from ciftools.binary.decoder import decode_cif_data
from ciftools.binary.encoding.impl.binary_cif_encoder import BinaryCIFEncoder
from ciftools.binary.encoding.impl.encoders.byte_array import BYTE_ARRAY_CIF_ENCODER
from numba import jit

from ciftools.binary.encoding.impl.encoders.integer_packing import INTEGER_PACKING_CIF_ENCODER

# TODO:
# Next - next encoder (quantization?)

# NOTE: Later:
# 2. function that produces inputs for decoding (sizes?) (negatives will be there or not?)
# 4. Test decoding - decode and decode optimized?
INPUT_DTYPE = 'i4'

INPUTS_FOR_ENCODING_NO_NEGATIVES = [
    # 0.8, 8, 80 MB
    np.random.randint(low=0, high=100, size=(2*10**5), dtype=INPUT_DTYPE),
    np.random.randint(low=0, high=100, size=(2*10**6), dtype=INPUT_DTYPE),
    # np.random.randint(low=0, high=100, size=(2*10**7), dtype=INPUT_DTYPE)
]

INPUTS_FOR_ENCODING_WITH_NEGATIVES = [
    np.random.randint(low=-50, high=50, size=(2*10**5), dtype=INPUT_DTYPE),
    np.random.randint(low=-50, high=50, size=(2*10**6), dtype=INPUT_DTYPE),
    # np.random.randint(low=-50, high=50, size=(2*10**7), dtype=INPUT_DTYPE)
]

def compute_inputs_for_decoding(inputs_for_encoding: list):
    inputs_for_decoding = []
    for input_arr in inputs_for_encoding:
        encoder = BinaryCIFEncoder([BYTE_ARRAY_CIF_ENCODER])
        encoded = encoder.encode_cif_data(input_arr)
        inputs_for_decoding.append(encoded)

    print(inputs_for_decoding)
    return inputs_for_decoding

# INPUTS_FOR_DECODING = compute_inputs_for_decoding()

OPTIMIZED = [False, True]

def int_packing_encoding(encoding_input, optimization):
    encoder = INTEGER_PACKING_CIF_ENCODER
    if not optimization:
        encoded = encoder.encode(encoding_input)
    else:
        encoded = encoder.encode_optimized(encoding_input)


@pytest.mark.parametrize("encoding_input", INPUTS_FOR_ENCODING_NO_NEGATIVES)
@pytest.mark.parametrize("optimization", OPTIMIZED)
def test_integer_packing_encoding_NO_negatives(benchmark, encoding_input, optimization):
    result = benchmark(int_packing_encoding, encoding_input=encoding_input, optimization=optimization)

# @pytest.mark.parametrize("encoding_input", INPUTS_FOR_ENCODING_WITH_NEGATIVES)
# @pytest.mark.parametrize("optimization", OPTIMIZED)
# def test_integer_packing_encoding_WITH_negatives(benchmark, encoding_input, optimization):
#     result = benchmark(int_packing_encoding, encoding_input=encoding_input, optimization=optimization)

