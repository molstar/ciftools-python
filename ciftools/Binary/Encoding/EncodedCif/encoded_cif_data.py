from typing import TypedDict

import numpy as np

from ciftools.Binary.Encoding import EncodingBase


class EncodedCIFData(TypedDict):
    encoding: list[EncodingBase]
    data: np.ndarray
