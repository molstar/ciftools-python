from argparse import ArgumentError
import pytest
import msgpack
import numpy as np
import random, string
from timeit import default_timer as timer

from ciftools.binary.encoder import INTEGER_PACKING

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

def encoding(encoding_input, optimization):
    encoder = INTEGER_PACKING
    if not optimization:
        encoded = encoder.encode_not_optimized(encoding_input)
    else:
        encoded = encoder.encode(encoding_input)

encoding_input = INPUTS_FOR_ENCODING[0]

start_not_optimized = timer()
encoding(encoding_input=encoding_input, optimization=False)
stop_not_optimized = timer()

start_not_optimized_2nd = timer()
encoding(encoding_input=encoding_input, optimization=False)
stop_not_optimized_2nd = timer()

start_not_optimized_3rd = timer()
encoding(encoding_input=encoding_input, optimization=False)
stop_not_optimized_3rd = timer()

start_optimized = timer()
encoding(encoding_input=encoding_input, optimization=True)
stop_optimized = timer()

start_optimized_2nd = timer()
encoding(encoding_input=encoding_input, optimization=True)
stop_optimized_2nd = timer()

start_optimized_3rd = timer()
encoding(encoding_input=encoding_input, optimization=True)
stop_optimized_3rd = timer()

not_optimized = stop_not_optimized - start_not_optimized
not_optimized_2nd = stop_not_optimized_2nd - start_not_optimized_2nd
not_optimized_3rd = stop_not_optimized_3rd - start_not_optimized_3rd

optimized = stop_optimized - start_optimized
optimized_2nd = stop_optimized_2nd - start_optimized_2nd
optimized_3rd = stop_optimized_3rd - start_optimized_3rd

print(not_optimized, not_optimized_2nd, not_optimized_3rd, optimized, optimized_2nd, optimized_3rd)
# 0.678212083876133 0.07555452641099691 0.0717478571459651 0.8585679298266768 0.12347683496773243 0.1249676188454032
# quite close to pytest-benchmark