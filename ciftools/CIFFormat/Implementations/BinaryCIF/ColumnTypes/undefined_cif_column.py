from __future__ import annotations  # supposed to be in python 3.10 but reverted; maybe in python 3.11?

from pydantic import BaseModel

from ciftools.CIFFormat.EValuePresence import EValuePresence
from ciftools.CIFFormat.i_cif_column import ICIFColumn


class UndefinedCIFColumn(ICIFColumn, BaseModel):
        @staticmethod
        def from_json(json: str) -> UndefinedCIFColumn:
            return UndefinedCIFColumn.parse_raw(json)

        def to_json(self) -> str:
            return self.json()

        def is_defined(self) -> bool:
            return False

        def get_string(self, row: int) -> str:
            return ""

        def get_integer(self, row: int) -> int:
            return 0

        def get_float(self, row: int) -> float:
            return 0.0

        def get_value_presence(self, row: int) -> EValuePresence:
            return EValuePresence.NotSpecified

        def are_values_equal(self, row_a: int, row_b: int) -> bool:
            return True

        def string_equals(self, row: int, value: str) -> bool:
            return value == ""
