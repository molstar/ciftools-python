from asyncore import write
from typing import Any, List
import unittest
from pathlib import Path

import numpy as np
from ciftools.binary.encoder import DELTA, INTEGER_PACKING, ComposeEncoders, FixedPoint

from ciftools.models.writer import CIFCategoryDesc, CIFFieldArrays, number_field, string_field
from ciftools.serialization import create_binary_writer, loads as loads_bcif

class TestMetadata:
    lattices_ids: np.ndarray


class TestVolumeData:
    metadata: TestMetadata
    volume: Any
    lattices: dict[int, np.ndarray]
    annotation: Any


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


LATTICE_IDS = CIFCategoryDesc(
    name="lattice_ids",
    fields=[
        number_field(
            name="id",
            dtype="i4",
            encoder=lambda _: INTEGER_PACKING,
            value=lambda data, i: data.metadata.lattices_ids[i],
        )
    ],
    get_count=lambda data: len(data.metadata.lattices_ids),
)

def create_volume_category(lattice_ids: List[int]):
    lattice_encoding = ComposeEncoders(FixedPoint(1000), DELTA, INTEGER_PACKING)

    def lattice_value_getter(lid: int):
        return lambda data, i: data.lattices[lid][i]

    fields = [
        number_field(
            name=f"lattice_{lid}",
            dtype="i4",
            encoder=lambda _: lattice_encoding,
            value=lattice_value_getter(lid),
        )
        for lid in lattice_ids
    ]
    fields.append(
        number_field(
            name=f"volume",
            dtype="f4",
            # TODO: use interval quantization
            encoder=lambda _: lattice_encoding,
            value=lambda data, i: data.volume[i],
        )
    )
    fields.append(
        number_field(
            name=f"volume_array",
            dtype="f4",
            encoder=lambda _: lattice_encoding,
            value=lambda data, i: data.volume[i],
            arrays=lambda data: CIFFieldArrays(values=data.volume),
        )
    )
    fields.append(string_field(name="annotation", value=lambda data, i: data.annotation[i]))

    return CIFCategoryDesc(
        name="volume",
        fields=fields,
        get_count=lambda data: len(data.volume),
    )

class TestEncodings_Encoding(unittest.TestCase):
    def test(self):

        # test
        test_data = prepare_test_data(5, 3)
        # print("Original data: " + str(test_data.__dict__))

        writer = create_binary_writer(encoder="ciftools-test")

        # write lattice ids
        writer.start_data_block("lattice_ids")
        writer.write_category(LATTICE_IDS, [test_data])


        writer.start_data_block("volume_data")
        writer.write_category(create_volume_category(test_data.metadata.lattices_ids), [test_data])

        encoded = writer.encode()
        (Path(__file__).parent / "lattices.bcif").write_bytes(encoded)

        # load encoded lattice ids
        parsed = loads_bcif(encoded, lazy=False)

        print("Decoded:")
        print(f"DataBlocks: {len(parsed.data_blocks)}")

        lattice_ids = (
            parsed["LATTICE_IDS"].lattice_ids.id.as_ndarray()
        )
        print(f"LatticeIds: {lattice_ids}")
        compare = np.array_equal(test_data.metadata.lattices_ids, lattice_ids)
        self.assertTrue(compare, "LatticeIds did not match original data")

        # load encoded data
        volume_and_lattices = parsed.VOLUME_DATA.volume

        print(f"Lattices: {volume_and_lattices.field_names}")
        volume = volume_and_lattices.volume.as_ndarray()
        print(f"Volume (parsed): {volume}")
        print(f"Volume (input): {test_data.volume}")
        compare = np.allclose(test_data.volume, volume, atol=1e-3)
        self.assertTrue(compare, "Volume did not match original data")

        volume_array = volume_and_lattices.volume_array.as_ndarray()
        print(f"Volume Array (parsed): {volume_array}")
        compare = np.allclose(test_data.volume, volume_array, atol=1e-3)
        self.assertTrue(compare, "Volume Array did not match original data")

        annotations = volume_and_lattices.annotation.as_ndarray()
        print(f"Annotations (parsed): {annotations}")
        print(f"Annotations (input): {test_data.annotation}")
        compare = np.array_equal(test_data.annotation, annotations)
        self.assertTrue(compare, "Annotations did not match original data")

        for lattice_id in lattice_ids:
            print(f"Lattice: {lattice_id}")
            lattice_value = volume_and_lattices[f"lattice_{lattice_id}"].as_ndarray()
            print(f"LatticeValue (parsed): {lattice_value}")
            print(f"LatticeValue (input): {test_data.lattices[lattice_id]}")
            compare = np.array_equal(test_data.lattices[lattice_id], lattice_value)
            self.assertTrue(compare, f"Lattice id {lattice_id} did not match original data")
