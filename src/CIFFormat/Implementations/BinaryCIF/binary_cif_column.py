from __future__ import annotations #supposed to be in python 3.10 but reverted; maybe in python 3.11?

from ...EValuePresence import EValuePresence
from ...i_cif_column import ICIFColumn


class BinaryCIFColumn(ICIFColumn):
    @staticmethod
    def from_json(json: str) -> BinaryCIFColumn:
        pass

    def to_json(self) -> str:
        pass

    def is_defined(self) -> bool:
        pass

    def get_string(self, row: int) -> str:
        pass

    def get_integer(self, row: int) -> int:
        pass

    def get_float(self, row: int) -> float:
        pass

    def get_value_presence(self, row: int) -> EValuePresence:
        pass

    def are_values_equal(self, row_a: int, row_b: int) -> bool:
        pass

    def string_equals(self, row: int, value: str) -> bool:
        pass
