from typing import Any, Callable, Optional

import numpy as np
from ciftools.binary.encoding import binarycif_encoder, encoders
from ciftools.binary.encoding.encoder import BinaryCIFEncoder
from ciftools.cif_format.value_presence import ValuePresenceEnum
from ciftools.writer.base import FieldDesc

_STRING_ARRAY_ENCODER = binarycif_encoder(encoders.STRING_ARRAY_CIF_ENCODER)


# TODO: derive from FieldDesc
class _StringFieldDesc:
    def create_array(self, total_count: int):
        return [""] * total_count

    def encoder(self, data: Any):
        return _STRING_ARRAY_ENCODER

    def __init__(
        self,
        name: str,
        value: Callable[[Any, int], Optional[int | float]],
        presence: Optional[Callable[[Any, int], Optional[ValuePresenceEnum]]] = None,
    ) -> None:
        self.name = name
        self.value = value
        self.presence = presence


def string_field(
    *,
    name: str,
    value: Callable[[Any, int], Optional[str]],
    presence: Optional[Callable[[Any, int], Optional[ValuePresenceEnum]]] = None,
) -> FieldDesc:
    return _StringFieldDesc(name=name, value=value, presence=presence)


# TODO: derive from FieldDesc
class _NumberFieldDesc:
    def create_array(self, total_count: int):
        return np.empty(total_count, dtype=self._dtype)

    def __init__(
        self,
        name: str,
        value: Callable[[Any, int], Optional[int | float]],
        dtype: np.dtype,
        encoder: Callable[[Any], BinaryCIFEncoder],
        presence: Optional[Callable[[Any, int], Optional[ValuePresenceEnum]]] = None,
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
    presence: Optional[Callable[[Any, int], Optional[ValuePresenceEnum]]] = None,
) -> FieldDesc:
    return _NumberFieldDesc(name=name, value=value, dtype=dtype, encoder=encoder, presence=presence)
