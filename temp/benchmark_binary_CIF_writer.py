
import numpy as np
from timeit import default_timer as timer
from ciftools.binary.writer import BinaryCIFWriter
from ciftools.serialization import create_binary_writer
from tests._encoding import prepare_test_data, LatticeIdsCategory

INPUTS_FOR_TESTING = [
    prepare_test_data(500000, 40)
]

print(f'Test data')
print(INPUTS_FOR_TESTING[0])

WRITER = create_binary_writer(encoder="ciftools-test")

# write lattice ids
WRITER.start_data_block("lattice_ids")

test_input = INPUTS_FOR_TESTING[0]

def benchmark_writer(test_input, optimization, writer: BinaryCIFWriter):
    if not optimization:
        writer.write_category_not_optimized(LatticeIdsCategory, [test_input])
    else:
        writer.write_category(LatticeIdsCategory, [test_input])



start_not_optimized = timer()
benchmark_writer(test_input=test_input, optimization=False, writer=WRITER)
stop_not_optimized = timer()

start_not_optimized_2nd = timer()
benchmark_writer(test_input=test_input, optimization=False, writer=WRITER)
stop_not_optimized_2nd = timer()

start_not_optimized_3rd = timer()
benchmark_writer(test_input=test_input, optimization=False, writer=WRITER)
stop_not_optimized_3rd = timer()

start_optimized = timer()
benchmark_writer(test_input=test_input, optimization=True, writer=WRITER)
stop_optimized = timer()

start_optimized_2nd = timer()
benchmark_writer(test_input=test_input, optimization=True, writer=WRITER)
stop_optimized_2nd = timer()

start_optimized_3rd = timer()
benchmark_writer(test_input=test_input, optimization=True, writer=WRITER)
stop_optimized_3rd = timer()

not_optimized = stop_not_optimized - start_not_optimized
not_optimized_2nd = stop_not_optimized_2nd - start_not_optimized_2nd
not_optimized_3rd = stop_not_optimized_3rd - start_not_optimized_3rd

optimized = stop_optimized - start_optimized
optimized_2nd = stop_optimized_2nd - start_optimized_2nd
optimized_3rd = stop_optimized_3rd - start_optimized_3rd

print(not_optimized, not_optimized_2nd, not_optimized_3rd, optimized, optimized_2nd, optimized_3rd)