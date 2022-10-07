from argparse import ArgumentError
from ciftools.binary.encoder import STRING_ARRAY
import pytest
import msgpack
import numpy as np
import random, string
from timeit import default_timer as timer

MAX_LENGTH = 30

def _random_string(length):
   return ''.join(random.choice(string.ascii_letters) for i in range(length))


# Source:
def _generate_random_strings_list(size: int):
    l = [_random_string(random.randint(1, MAX_LENGTH)) for i in range(size)]
    return l
    
INPUTS_FOR_ENCODING = [
    # roughly 0.8, 8, 80 MB
    _generate_random_strings_list(10**5),
    # _generate_random_strings_list(10**6),
    # _generate_random_strings_list(10**7)
]

OPTIMIZED = [True, False]

def _pre_run_encode():
    encoder = STRING_ARRAY
    encoded = encoder.encode(INPUTS_FOR_ENCODING[0])

_pre_run_encode()

def encoding(encoding_input, optimization):
    encoder = STRING_ARRAY
    if not optimization:
        encoded = encoder.encode_not_optimized(encoding_input)
    else:
        encoded = encoder.encode(encoding_input)


@pytest.mark.parametrize("encoding_input", INPUTS_FOR_ENCODING)
@pytest.mark.parametrize("optimization", OPTIMIZED)
def test_encoding(benchmark, encoding_input, optimization):
    result = benchmark(encoding, encoding_input=encoding_input, optimization=optimization)


