import numpy as np


class TestMetadata:
    lattices_ids: np.ndarray


class TestVolumeData:
    metadata: TestMetadata
    volume: any
    lattices: dict[int, np.ndarray]
    annotation: any


def prepare_test_data(size: int, num_lattices=2) -> TestVolumeData:
    data = TestVolumeData()
    data.lattices = dict()
    data.metadata = TestMetadata()
    data.metadata.lattices_ids = list(range(num_lattices))
    for i in data.metadata.lattices_ids:
        data.lattices[i] = np.arange(size) + i

    data.volume = np.array([0.123 + 0.1 * i for i in range(size)])
    data.annotation = [f"Annotation {i}" for i in range(size)]

    return data
