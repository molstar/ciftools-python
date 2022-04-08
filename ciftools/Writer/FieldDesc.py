import abc
from typing import Optional, Union

import numpy as np
from ciftools.Binary.Encoding.Encoder import BinaryCIFEncoder
from ciftools.CIFFormat.EValuePresence import EValuePresence


class FieldDesc(abc.ABC):
    name: str

    @abc.abstractmethod
    def has_string(self) -> bool:
        pass

    @abc.abstractmethod
    def string(self, data: any, i: int) -> Optional[str]:
        pass

    @abc.abstractmethod
    def has_number(self) -> bool:
        pass

    @abc.abstractmethod
    def number(self, data: any, i: int) -> Optional[Union[int, float]]:
        pass

    @abc.abstractmethod
    def has_typed_array(self) -> bool:
        pass

    @abc.abstractmethod
    def typed_array(self, total_count: int) -> np.ndarray:
        pass

    @abc.abstractmethod
    def encoder(self) -> BinaryCIFEncoder:
        pass

    @abc.abstractmethod
    def has_presence(self) -> bool:
        pass

    @abc.abstractmethod
    def presence(self, data: any, i: int) -> EValuePresence:
        pass
