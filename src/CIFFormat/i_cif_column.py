import abc

from .EValuePresence import EValuePresence
from ..JsonSerialization.i_json_serializable import IJsonSerializable

class ICIFColumn(abc.ABC, IJsonSerializable):
    @abc.abstractmethod
    def is_defined(self) -> bool:
        pass

    @abc.abstractmethod
    def get_string(self, row: int) -> str:
        pass

    @abc.abstractmethod
    def get_integer(self, row: int) -> int:
        pass

    @abc.abstractmethod
    def get_float(self, row: int) -> float:
        pass

    @abc.abstractmethod
    def get_value_presence(self, row: int) -> EValuePresence:
        pass

    @abc.abstractmethod
    def are_values_equal(self, row_a: int, row_b: int) -> bool:
        pass

    @abc.abstractmethod
    def string_equals(self, row: int, value: str) -> bool:
        pass