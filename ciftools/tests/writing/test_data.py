import numpy as np


class TestMetadata:
    lattices_ids: np.ndarray


class TestVolumeData:
    metadata: TestMetadata
    volume: any
    lattices: dict[int, np.ndarray]


def prepare_test_data(size: int) -> TestVolumeData:
    data = TestVolumeData()
    data.lattices = dict()
    data.metadata = TestMetadata()
    data.metadata.lattices_ids = [1, 2, 3, 15, 107]
    for i in data.metadata.lattices_ids:
        data.lattices[i] = np.random.randint(1, 100, size)

    data.volume = np.random.randint(1, 100, size)

    return data
