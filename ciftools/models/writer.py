from dataclasses import dataclass
from typing import Any, Callable, List, Optional, Protocol, Union

import numpy as np
from ciftools.binary.encoding.impl.binary_cif_encoder import BinaryCIFEncoder
from ciftools.models.data import CIFValuePresenceEnum


@dataclass
class CIFFieldArrays:
    values: Union[np.ndarray, List[str], List[int], List[float]]
    """Array of the values themselves"""
    mask: Optional[np.ndarray] = None
    """Optional uint8 array for specifying the missing values. 0 = defined, 1 = ., 2 = ?"""


@dataclass
class CIFFieldDesc:
    name: str
    create_array: Callable[[int], np.ndarray]
    encoder: Callable[[Any], BinaryCIFEncoder]
    value: Optional[Callable[[Any, int], Any]] = None
    presence: Optional[Callable[[Any, int], CIFValuePresenceEnum]] = None
    arrays: Optional[Callable[[Any], CIFFieldArrays]] = None


@dataclass
class CIFCategoryDesc:
    name: str
    fields: List[CIFFieldDesc]


@dataclass
class CIFCategoryData:
    count: int = 1
    data: Optional[Any] = None


class CIFWriter(Protocol):
    def start_data_block(self, header: str) -> None:
        ...

    def write_category(self, category: CIFCategoryDesc, data: List[CIFCategoryData]) -> None:
        ...

    def encode(self) -> Union[str, bytes]:
        ...
