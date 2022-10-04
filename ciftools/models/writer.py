from dataclasses import dataclass
from typing import Any, Callable, List, Optional, Protocol, Union

import numpy as np
from ciftools.binary.encoder import BYTE_ARRAY, STRING_ARRAY, BinaryCIFEncoder
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
    create_array: Callable[[int], Union[np.ndarray, List[str]]]
    encoder: Callable[[Any], BinaryCIFEncoder]
    value: Optional[Callable[[Any, int], Any]] = None
    presence: Optional[Callable[[Any, int], CIFValuePresenceEnum]] = None
    arrays: Optional[Callable[[Any], CIFFieldArrays]] = None


@dataclass
class CIFCategoryDesc:
    name: str
    fields: List[CIFFieldDesc]
    get_count: Callable[[Any], int]


class CIFWriter(Protocol):
    def start_data_block(self, header: str) -> None:
        ...

    def write_category(self, category: CIFCategoryDesc, data: List[Any]) -> None:
        ...

    def encode(self) -> Union[str, bytes]:
        ...


def number_field(
    *,
    name: str,
    value: Optional[Callable[[Any, int], Optional[Union[int, float]]]] = None,
    dtype: Union[np.dtype, str],
    encoder: Callable[[Any], BinaryCIFEncoder] = lambda data: BYTE_ARRAY,
    presence: Optional[Callable[[Any, int], CIFValuePresenceEnum]] = None,
) -> CIFFieldDesc:
    return CIFFieldDesc(
        name=name,
        value=value,
        create_array=lambda size: np.empty(size, dtype=dtype),
        encoder=encoder,
        presence=presence,
    )


def number_array_field(
    *,
    name: str,
    dtype: Union[np.dtype, str],
    encoder: Callable[[Any], BinaryCIFEncoder] = lambda data: BYTE_ARRAY,
    arrays: Optional[Callable[[Any], CIFFieldArrays]] = None,
) -> CIFFieldDesc:
    return CIFFieldDesc(
        name=name,
        create_array=lambda size: np.empty(size, dtype=dtype),
        encoder=encoder,
        arrays=arrays,
    )


def string_field(
    *,
    name: str,
    value: Callable[[Any, int], Optional[str]] = None,
    presence: Optional[Callable[[Any, int], CIFValuePresenceEnum]] = None,
) -> CIFFieldDesc:
    return CIFFieldDesc(
        name=name,
        value=value,
        create_array=lambda size: [""] * size,
        encoder=lambda _: STRING_ARRAY,
        presence=presence,
    )


def string_array_field(
    *,
    name: str,
    arrays: Optional[Callable[[Any], CIFFieldArrays]] = None,
) -> CIFFieldDesc:
    return CIFFieldDesc(
        name=name,
        create_array=lambda size: [""] * size,
        encoder=lambda _: STRING_ARRAY,
        arrays=arrays,
    )
