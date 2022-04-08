import unittest
from pathlib import Path

import numpy as np
from ciftools.Binary.Writer.BinaryCIFWriter import BinaryCIFWriter
from ciftools.CIFFormat.Implementations.BinaryCIF.binary_cif_file import BinaryCIFFile
from ciftools.tests.writing.Fields.lattice import TestFieldDesc_Lattice
from ciftools.tests.writing.Fields.lattice_ids import TestFieldDesc_LatticeIds
from ciftools.tests.writing.Fields.volume import TestFieldDesc_Volume
from ciftools.tests.writing.test_data import TestVolumeData, prepare_test_data
from ciftools.Writer.CategoryDesc import CategoryDesc
from ciftools.Writer.CategoryWriter import CategoryWriter
from ciftools.Writer.CategoryWriterProvider import CategoryWriterProvider
from ciftools.Writer.FieldDesc import FieldDesc
from ciftools.Writer.OutputStream import OutputStream


class TestCategoryDesc(CategoryDesc):
    def __init__(self, name: str, fields: list[FieldDesc]):
        self.name = name
        self.fields = fields


class TestCategoryWriter(CategoryWriter):
    def __init__(self, data: TestVolumeData, count: int, category_desc: TestCategoryDesc):
        self.data = data
        self.count = count
        self.desc = category_desc


class TestCategoryWriterProvider_LatticeIds(CategoryWriterProvider):
    length: int

    def __init__(self, length: int):
        self.length = length

    def category_writer(self, ctx: TestVolumeData) -> CategoryWriter:
        field_desc: list[FieldDesc] = [TestFieldDesc_LatticeIds()]
        return TestCategoryWriter(ctx, self.length, TestCategoryDesc("lattice_ids", field_desc))


class TestCategoryWriterProvider_Volume(CategoryWriterProvider):
    length: int

    def __init__(self, length: int):
        self.length = length

    def category_writer(self, ctx: TestVolumeData) -> CategoryWriter:
        field_desc: list[FieldDesc] = [TestFieldDesc_Lattice(_id) for _id in ctx.metadata.lattices_ids]
        field_desc.append(TestFieldDesc_Volume())

        return TestCategoryWriter(ctx, self.length, TestCategoryDesc("volume", field_desc))


class TestOutputStream(OutputStream):
    encoded_output = None

    def write_string(self, data: str) -> bool:
        self.encoded_output = data
        return True

    def write_binary(self, data: np.ndarray) -> bool:
        self.encoded_output = data
        return True


class TestEncodings_Encoding(unittest.TestCase):
    def test(self):

        # test
        test_data = prepare_test_data(5, 1)
        # print("Original data: " + str(test_data.__dict__))

        writer = BinaryCIFWriter("my_encoder")

        # write lattice ids
        category_writer_provider = TestCategoryWriterProvider_LatticeIds(len(test_data.metadata.lattices_ids))
        writer.start_data_block("lattice_ids")
        writer.write_category(category_writer_provider, [test_data])

        # write lattices and volume
        category_writer_provider = TestCategoryWriterProvider_Volume(len(test_data.volume))
        writer.start_data_block("volume_data")
        writer.write_category(category_writer_provider, [test_data])

        # encode and flush
        writer.encode()
        output_stream = TestOutputStream()
        writer.flush(output_stream)

        encoded = output_stream.encoded_output
        (Path(__file__).parent / "lattices.bcif").write_bytes(encoded)

        # load encoded lattice ids
        parsed = BinaryCIFFile.loads(encoded, lazy=False)

        print("Decoded:")
        print("DataBlocks: " + str(len(parsed.data_blocks)))

        # TODO: missing initial character a from category name -> bug may be in the encoder?
        lattice_ids = (
            parsed.data_block("lattice_ids".upper())
            .get_category("lattice_ids")
            .get_column("lattice_ids")
            .__dict__["_values"]
        )
        print("LatticeIds: " + str(lattice_ids))
        compare = np.array_equal(test_data.metadata.lattices_ids, lattice_ids)
        self.assertTrue(compare, "LatticeIds did not match original data")

        # load encoded data
        volume_and_lattices = parsed.data_block("volume_data".upper()).get_category("volume")

        print("Lattices: " + str(volume_and_lattices.column_names()))
        volume = volume_and_lattices.get_column("volume").__dict__["_values"]
        print("Volume (parsed): " + str(volume))
        print("Volume (input): " + str(test_data.volume))
        compare = np.allclose(test_data.volume, volume, atol=1e-3)
        self.assertTrue(compare, "Volume did not match original data")

        for lattice_id in lattice_ids:
            print("Lattice: " + str(lattice_id))
            lattice_value = volume_and_lattices.get_column("lattice_" + str(lattice_id)).__dict__["_values"]
            print("LatticeValue (parsed): " + str(lattice_value))
            print("LatticeValue (input): " + str(test_data.lattices[lattice_id]))
            compare = np.array_equal(test_data.lattices[lattice_id], lattice_value)
            self.assertTrue(compare, str("Lattice id " + str(lattice_id) + " did not match original data"))
