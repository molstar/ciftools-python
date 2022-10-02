from typing import Optional, TypedDict, Union

import numpy as np
from ciftools.binary.encoding_types import EncodingBase


class EncodedCIFData(TypedDict):
    encoding: list[EncodingBase]
    data: Union[bytes, np.ndarray]


class EncodedCIFColumn(TypedDict):
    name: str
    data: EncodedCIFData
    mask: Optional[EncodedCIFData]


class EncodedCIFCategory(TypedDict):
    name: str
    rowCount: int
    columns: list[EncodedCIFColumn]


class EncodedCIFDataBlock(TypedDict):
    header: str
    categories: list[EncodedCIFCategory]


class EncodedCIFFile(TypedDict):
    version: str
    encoder: str
    dataBlocks: list[EncodedCIFDataBlock]
