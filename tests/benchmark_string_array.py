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
def _generate_random_strings_list(size: int, n_of_strings: int):
    l = [_random_string(random.randint(1, MAX_LENGTH)) for i in range(n_of_strings)]
    repeated_l = l * size
    return repeated_l

INPUTS_FOR_ENCODING = {}

for n_of_strings in [20, 50, 100]:
    for size in [10**4, 10**5, 10**6]:
        INPUTS_FOR_ENCODING[f'{n_of_strings}_{size}'] = _generate_random_strings_list(size=size, n_of_strings=n_of_strings)

def encoding(encoding_input, optimization):
    encoder = STRING_ARRAY
    if not optimization:
        encoded = encoder.encode_not_optimized(encoding_input)
    else:
        encoded = encoder.encode(encoding_input)

print('not_optimized, not_optimized_2nd, not_optimized_3rd, optimized, optimized_2nd, optimized_3rd')
for case_name, encoding_input in INPUTS_FOR_ENCODING.items():

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

    print(case_name)
    print(not_optimized, not_optimized_2nd, not_optimized_3rd, optimized, optimized_2nd, optimized_3rd)

# print(not_optimized, not_optimized_2nd, not_optimized_3rd, optimized, optimized_2nd, optimized_3rd)
# 0.678212083876133 0.07555452641099691 0.0717478571459651 0.8585679298266768 0.12347683496773243 0.1249676188454032
# quite close to pytest-benchmark

# NO JIT
# not_optimized, not_optimized_2nd, not_optimized_3rd, optimized, optimized_2nd, optimized_3rd
# 20_10000
# 2.671183445956558 0.037990274955518544 0.038723392062820494 0.02901634795125574 0.027696584002114832 0.027359343017451465
# 20_100000
# 0.35828070098068565 0.35529211803805083 0.3570930790156126 0.2672198748914525 0.26997689506970346 0.26407589903101325
# 20_1000000
# 3.754518774920143 3.6613519359380007 3.590928812045604 2.7633999809622765 2.742795309983194 2.7856404760386795
# 50_10000
# 0.08946576493326575 0.08893638011068106 0.08875931904185563 0.05730705999303609 0.05827989405952394 0.05729172995779663
# 50_100000
# 0.886467493022792 0.8783201409969479 0.884077426046133 0.7304035819834098 0.7092675910098478 0.7059366019675508
# 50_1000000
# 9.578126006992534 9.592585199978203 9.336758888093755 7.011043209931813 6.888902453938499 6.8985374378971756
# 100_10000
# 0.17676137096714228 0.1785169130889699 0.17561967996880412 0.12274663499556482 0.12944400194101036 0.12680783797986805
# 100_100000
# 1.7786761060124263 1.7187940969597548 1.7390421900199726 1.4047608590917662 1.4061879760120064 1.3963392629520968
# 100_1000000
# 17.475244562956505 17.666481979074888 17.797239091945812 13.829927618033253 13.793060117051937 13.868345592985861