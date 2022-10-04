from enum import IntEnum
from typing import Any, Dict, List, Optional, Protocol, Union

import numpy as np


class CIFValuePresenceEnum(IntEnum):
    Present = 0
    NotSpecified = 1
    Unknown = 2


class CIFColumn(Protocol):
    def get_string(self, row: int) -> Optional[str]:
        ...

    def get_integer(self, row: int) -> int:
        ...

    def get_float(self, row: int) -> float:
        ...

    def get_value_presence(self, row: int) -> CIFValuePresenceEnum:
        ...

    def are_values_equal(self, row_a: int, row_b: int) -> bool:
        ...

    def string_equals(self, row: int, value: str) -> bool:
        ...

    def as_ndarray(
        self, *, dtype: Optional[Union[np.dtype, str]] = None, start: Optional[int] = None, end: Optional[int] = None
    ) -> np.ndarray:
        """
        Return the column represented as a numpy array.
        
        - If dtype is specified, a copy of the underlying array is returned.
        - Otherwise returns a view of the underlying data.
        """
        ...

    def __getitem__(self, idx: Any) -> Any:
        ...

    def __len__(self) -> int:
        ...

    @property
    def value_presences(self) -> Optional[np.ndarray]:
        """
        Presences represented as numpy byte array (see `CIFValuePresenceEnum` explanation)
        """
        ...


class CIFCategory(Protocol):
    @property
    def name(self) -> str:
        ...

    @property
    def n_rows(self) -> int:
        ...

    @property
    def n_columns(self) -> int:
        ...

    @property
    def field_names(self) -> List[str]:
        ...

    def __getattr__(self, name: str) -> CIFColumn:
        return self[name]

    def __getitem__(self, name: str) -> CIFColumn:
        ...

    def __contains__(self, key: str) -> bool:
        ...

    # Category Helpers
    def get_matrix(self, field: str, rows: int, cols: int, row_index: int) -> np.ndarray:
        """
        Extracts a  matrix from a category from a specified row_index.

        _category.matrix[1][1]: v11
        ....
        ....
        _category.matrix[rows][cols]: vRowsCols
        """
        matrix = np.empty((rows, cols), float)
        for i in range(1, rows + 1):
            row = np.empty(cols)
            for j in range(1, cols + 1):
                row[j - 1] = self[f"{field}[{i}][{j}]"].get_float(row_index)

            matrix[i - 1] = row

        return matrix

    def get_vector(self, field: str, rows: int, cols: int, row_index: int) -> np.ndarray:
        """
        Extracts a vector from a category from a specified row_index.

        _category.matrix[1][1]: v11
        ....
        ....
        _category.matrix[rows][cols]: vRowsCols
        """
        vector = np.empty(rows, float)
        for i in range(1, rows + 1):
            vector[i - 1] = self[f"{field}[{i}]"].get_float(row_index)

        return vector


class CIFDataBlock(Protocol):
    def __getattr__(self, name: str) -> CIFCategory:
        return self[name]

    def __getitem__(self, name: str) -> CIFCategory:
        ...

    def __contains__(self, key: str):
        ...

    @property
    def header(self) -> str:
        ...

    @property
    def categories(self) -> Dict[str, CIFCategory]:
        ...


class CIFFile(Protocol):
    def __getitem__(self, index_or_name: Union[int, str]) -> CIFDataBlock:
        """
        Access a data block by index or header (case sensitive)
        """
        ...

    def __getattr__(self, name: str) -> CIFDataBlock:
        return self[name]

    def __len__(self) -> int:
        ...

    def __contains__(self, key: str) -> bool:
        return key in self._block_map

    @property
    def data_blocks(self) -> List[CIFDataBlock]:
        ...
