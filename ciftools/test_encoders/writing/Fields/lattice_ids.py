from typing import Optional, Union

import numpy as np
from numpy import int32

from ciftools.Binary.Encoding.Encoder import BinaryCIFEncoder
from ciftools.Binary.Encoding.Encoders.Delta_CIFEncoder import Delta_CIFEncoder
from ciftools.Binary.Encoding.Encoders.ICIFEncoder import ICIFEncoder
from ciftools.Binary.Encoding.Encoders.IntegerPacking_CIFEncoder import IntegerPacking_CIFEncoder
from ciftools.Binary.Encoding.Encoders.RunLength_CIFEncoder import RunLength_CIFEncoder
from ciftools.CIFFormat.EValuePresence import EValuePresence
from ciftools.Writer.FieldDesc import FieldDesc
from ciftools.test_encoders.writing.test_data import TestVolumeData


class TestFieldDesc_LatticeIds(FieldDesc):
    def __init__(self):
        self.name = "lattice_ids"

    def has_string(self) -> bool:
        return False

    def string(self, data: TestVolumeData, i: int) -> Optional[str]:
        pass

    def has_number(self) -> bool:
        return True

    def number(self, data: TestVolumeData, i: int) -> Optional[Union[int, float]]:
        return data.metadata.lattices_ids[i]

    def has_typed_array(self) -> bool:
        return True

    def typed_array(self, total_count: int) -> np.ndarray:
        return np.ndarray([total_count], dtype=np.dtype(int32))

    def encoder(self) -> BinaryCIFEncoder:
        return BinaryCIFEncoder.by(IntegerPacking_CIFEncoder())

    def has_presence(self) -> bool:
        return True

    def presence(self, data: TestVolumeData, i: int) -> EValuePresence:
        return EValuePresence.Present