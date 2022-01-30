from __future__ import annotations #supposed to be in python 3.10 but reverted; maybe in python 3.11?

from ...i_cif_category import ICIFCategory
from ...i_cif_column import ICIFColumn


class BinaryCIFCategory(ICIFCategory):
    @staticmethod
    def from_json(json: str) -> BinaryCIFCategory:
        pass

    def to_json(self) -> str:
        pass

    def name(self) -> str:
        pass

    def row_count(self) -> int:
        pass

    def column_count(self) -> int:
        pass

    def column_names(self) -> [str]:
        pass

    def get_column(self, name: str) -> ICIFColumn:
        pass

    def get_matrix(self, field: str, rows: int, cols: int, row_index: int):
        pass

    def get_vector(self, field: str, rows: int, cols: int, row_index: int) -> [int]:
        pass

