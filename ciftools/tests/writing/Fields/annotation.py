from typing import Optional, Union

import numpy as np
from ciftools.Binary.Encoding.Encoder import BinaryCIFEncoder
from ciftools.Binary.Encoding.Encoders.StringArray_CIFEncoder import StringArray_CIFEncoder
from ciftools.CIFFormat.EValuePresence import EValuePresence
from ciftools.tests.writing.test_data import TestVolumeData
from ciftools.Writer.FieldDesc import FieldDesc


class TestFieldDesc_Annotation(FieldDesc):
    def __init__(self):
        self.name = "annotation"

    def has_string(self) -> bool:
        return True

    def string(self, data: TestVolumeData, i: int) -> Optional[str]:
        return data.annotation[i]

    def has_number(self) -> bool:
        return False

    def number(self, data: TestVolumeData, i: int) -> Optional[Union[int, float]]:
        pass

    def has_typed_array(self) -> bool:
        return False

    def typed_array(self, total_count: int) -> np.ndarray:
        pass
        # NOTE: a hack to get strings as typed arrays
        # return np.ndarray([total_count], dtype=np.object_)

    def encoder(self) -> BinaryCIFEncoder:
        return BinaryCIFEncoder.by(StringArray_CIFEncoder())

    def has_presence(self) -> bool:
        return False

    def presence(self, data: TestVolumeData, i: int) -> EValuePresence:
        pass
