from dataclasses import dataclass
from typing import Any, Callable, Collection, Generic, List, Optional, Protocol, TypeVar, Union

import numpy as np
from ciftools.binary.encoder import BYTE_ARRAY, STRING_ARRAY, BinaryCIFEncoder
from ciftools.models.data import CIFValuePresenceEnum

TData = TypeVar("TData")
TArrays = Union[np.ndarray, List[str], List[int], List[float]]


@dataclass
class CIFFieldDesc(Generic[TData]):
    name: str
    create_array: Callable[[int], Union[np.ndarray, List[str]]]
    encoder: Callable[[Any], BinaryCIFEncoder]
    value: Optional[Callable[[Any, int], Any]] = None
    presence: Optional[Callable[[Any, int], CIFValuePresenceEnum]] = None
    value_array: Optional[Callable[[Any], TArrays]] = None
    presence_array: Optional[Callable[[Any], Optional[np.ndarray]]] = None
    """Optional uint8 array for specifying the missing values. 0 = defined, 1 = ., 2 = ?"""

    @staticmethod
    def numbers(
        *,
        name: str,
        value: Optional[Callable[[TData, int], Optional[Union[int, float]]]] = None,
        dtype: Union[np.dtype, str],
        encoder: Callable[[TData], BinaryCIFEncoder] = lambda data: BYTE_ARRAY,
        presence: Optional[Callable[[TData, int], CIFValuePresenceEnum]] = None,
    ) -> "CIFFieldDesc":
        return CIFFieldDesc(
            name=name,
            value=value,
            create_array=lambda size: np.empty(size, dtype=dtype),
            encoder=encoder,
            presence=presence,
        )

    @staticmethod
    def number_array(
        *,
        name: str,
        dtype: Union[np.dtype, str],
        encoder: Callable[[TData], BinaryCIFEncoder] = lambda _: BYTE_ARRAY,
        array: Callable[[TData], TArrays],
        presence: Optional[Callable[[TData], Optional[np.ndarray]]] = None,
    ) -> "CIFFieldDesc":
        return CIFFieldDesc(
            name=name,
            create_array=lambda size: np.empty(size, dtype=dtype),
            encoder=encoder,
            value_array=array,
            presence_array=presence,
        )

    @staticmethod
    def strings(
        *,
        name: str,
        value: Callable[[TData, int], Optional[str]] = None,
        presence: Optional[Callable[[TData, int], CIFValuePresenceEnum]] = None,
    ) -> "CIFFieldDesc":
        return CIFFieldDesc(
            name=name,
            value=value,
            create_array=lambda size: [""] * size,
            encoder=lambda _: STRING_ARRAY,
            presence=presence,
        )

    @staticmethod
    def string_array(
        *,
        name: str,
        array: Optional[Callable[[TData], TArrays]] = None,
        mask: Optional[Callable[[TData], Optional[np.ndarray]]] = None,
    ) -> "CIFFieldDesc":
        return CIFFieldDesc(
            name=name,
            create_array=lambda size: [""] * size,
            encoder=lambda _: STRING_ARRAY,
            value_array=array,
            presence_array=mask,
        )


class CIFCategoryDesc(Protocol):
    @property
    def name(self) -> str:
        ...

    @staticmethod
    def get_row_count(data: Any) -> int:
        ...

    @staticmethod
    def get_field_descriptors(data: Any) -> Collection[CIFFieldDesc]:
        ...


class CIFWriter(Protocol):
    def start_data_block(self, header: str) -> None:
        ...

    def write_category(self, category: CIFCategoryDesc, data: List[Any]) -> None:
        ...

    def encode(self) -> Union[str, bytes]:
        ...
