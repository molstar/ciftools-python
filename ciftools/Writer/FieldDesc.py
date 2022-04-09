import abc
import numpy as np
from typing import Callable, Optional, Union, Any

import numpy as np
from ciftools.Binary.Encoding.encoder import BinaryCIFEncoder
from ciftools.CIFFormat.EValuePresence import EValuePresence
from ciftools.Binary.Encoding.Encoders.string_array import StringArrayCIFEncoder


class FieldDesc(abc.ABC):
    name: str

    @abc.abstractmethod
    def create_array(self, total_count: int) -> np.ndarray | list:
        pass

    @abc.abstractmethod
    def value(self, data: Any, i: int) -> Any:
        pass

    @abc.abstractmethod
    def encoder(self, data: Any) -> BinaryCIFEncoder:
        pass

    @abc.abstractmethod
    def presence(self, data: any, i: int) -> EValuePresence:
        pass


_STRING_ARRAY_ENCODER = BinaryCIFEncoder.by(StringArrayCIFEncoder())


#TODO: derive from FieldDesc
class StringFieldDesc:
    def create_array(self, total_count: int):
        return [""] * total_count

    def encoder(self, data: Any):
        return _STRING_ARRAY_ENCODER

    def __init__(
        self,
        name: str,
        value: Callable[[Any, int], Optional[int | float]],
        presence: Optional[Callable[[Any, int], Optional[EValuePresence]]] = None,
    ) -> None:
        self.name = name
        self.value = value
        self.presence = presence


def string_field(
    *,
    name: str,
    value: Callable[[Any, int], Optional[str]],
    presence: Optional[Callable[[Any, int], Optional[EValuePresence]]] = None,
):
    return StringFieldDesc(name=name, value=value, presence=presence)


#TODO: derive from FieldDesc
class NumberFieldDesc:
    def create_array(self, total_count: int):
        return np.empty(total_count, dtype=self._dtype)

    def __init__(
        self,
        name: str,
        value: Callable[[Any, int], Optional[int | float]],
        dtype: np.dtype,
        encoder: Callable[[Any], BinaryCIFEncoder],
        presence: Optional[Callable[[Any, int], Optional[EValuePresence]]] = None,
    ) -> None:
        self.name = name
        self.value = value
        self._dtype = dtype
        self.encoder = encoder
        self.presence = presence


def number_field(
    *,
    name: str,
    value: Callable[[Any, int], Optional[int | float]],
    dtype: np.dtype,
    encoder: Callable[[Any], BinaryCIFEncoder],
    presence: Optional[Callable[[Any, int], Optional[EValuePresence]]] = None,
):
    return NumberFieldDesc(name=name, value=value, dtype=dtype, encoder=encoder, presence=presence)
