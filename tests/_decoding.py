import unittest
import urllib.request
from pathlib import Path

from ciftools.models.data import CIFValuePresenceEnum
from ciftools.serialization import loads

test_folder = Path(__file__).parent / "fixtures"


class TestEncodings_Decoding(unittest.TestCase):
    def test(self):
        # TODO: set assert expectations

        print("mmCIF test")
        bcif_path = test_folder / "1tqn.bcif"
        data = bcif_path.read_bytes()
        parsed = loads(data, lazy=False)

        atom_site = parsed["1TQN"].atom_site
        entity = parsed[0]["entity"]
        label_comp_id = atom_site.label_comp_id
        cartn_x = atom_site["Cartn_x"]

        print("id" in entity)  # test if field is present in category
        print("atom_site" in parsed[0])  # test if category is present data block
        print(entity.field_names)
        print(atom_site.n_rows)
        print(label_comp_id[0])
        print(label_comp_id[-1])
        print(len(label_comp_id))
        print(cartn_x[0:10])
        value_slice = cartn_x.as_ndarray(start=1, end=10, dtype="i4")
        print(value_slice)
        print(atom_site["label_alt_id"].value_presences[0] == CIFValuePresenceEnum.NotSpecified)
        # print([[f"_{c.name}.{f}" for f in c.field_names] for c in parsed[0].categories.values()])

        print("Volume Data test")
        bcif_path = test_folder / "x-ray_1tqn-cartn_-22.4_-33.4_-21.6_-7.1_-10_-0.9_d1.bcif"
        data = bcif_path.read_bytes()
        parsed = loads(data)

        print([b.header for b in parsed.data_blocks])
        print(parsed[1].categories.keys())
        print(parsed["FO-FC"].categories.keys())
        print(parsed[1]["volume_data_3d_info"].field_names)
        print(parsed[1]["volume_data_3d"].n_rows)
        print(parsed[1]["volume_data_3d"]["values"][0:10])
