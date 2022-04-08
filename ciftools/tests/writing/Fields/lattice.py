from typing import Optional, Union

import numpy as np
from ciftools.Binary.Encoding.Encoder import BinaryCIFEncoder
from ciftools.Binary.Encoding.Encoders.Delta_CIFEncoder import Delta_CIFEncoder
from ciftools.Binary.Encoding.Encoders.FixedPoint_CIFEncoder import FixedPoint_CIFEncoder
from ciftools.Binary.Encoding.Encoders.ICIFEncoder import ICIFEncoder
from ciftools.Binary.Encoding.Encoders.IntegerPacking_CIFEncoder import IntegerPacking_CIFEncoder
from ciftools.CIFFormat.EValuePresence import EValuePresence
from ciftools.tests.writing.test_data import TestVolumeData
from ciftools.Writer.FieldDesc import FieldDesc
from numpy import int32


class TestFieldDesc_Lattice(FieldDesc):
    lattice_id: int

    def __init__(self, lattice_id: int):
        self.name = "lattice_" + str(lattice_id)
        self.lattice_id = lattice_id

    def has_string(self) -> bool:
        return False

    def string(self, data: TestVolumeData, i: int) -> Optional[str]:
        pass

    def has_number(self) -> bool:
        return True

    def number(self, data: TestVolumeData, i: int) -> Optional[Union[int, float]]:
        return data.lattices[self.lattice_id][i]

    def has_typed_array(self) -> bool:
        return True

    def typed_array(self, total_count: int) -> np.ndarray:
        return np.ndarray([total_count], dtype=np.dtype(int32))

    def encoder(self) -> BinaryCIFEncoder:
        return (
            BinaryCIFEncoder.by(FixedPoint_CIFEncoder(1000)).and_(Delta_CIFEncoder()).and_(IntegerPacking_CIFEncoder())
        )

    def has_presence(self) -> bool:
        return False

    def presence(self, data: TestVolumeData, i: int) -> EValuePresence:
        pass
