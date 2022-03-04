from typing import TypedDict

import numpy as np

from ...Binary.Encoding import EncodingBase


class EncodedCIFData(TypedDict):
    encoding: list[EncodingBase]
    data: np.ndarray
