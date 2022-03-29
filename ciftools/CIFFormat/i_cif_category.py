import abc

import numpy as np

from ..JsonSerialization.i_json_serializable import IJsonSerializable
from .i_cif_column import ICIFColumn


class ICIFCategory(IJsonSerializable, abc.ABC):
    @abc.abstractmethod
    def name(self) -> str:
        pass

    @abc.abstractmethod
    def row_count(self) -> int:
        pass

    @abc.abstractmethod
    def column_count(self) -> int:
        pass

    @abc.abstractmethod
    def column_names(self) -> list[str]:
        pass

    @abc.abstractmethod
    def get_column(self, name: str) -> ICIFColumn:
        pass

    # Category Helpers

    # Extracts a  matrix from a category from a specified row_index.
    #
    # _category.matrix[1][1]: v11
    # ....
    # ....
    # _category.matrix[rows][cols]: vRowsCols
    #

    @staticmethod
    def get_matrix(self, field: str, rows: int, cols: int, row_index: int) -> np.ndarray:
        matrix = np.empty((rows, cols), float)
        for i in range(1, rows + 1):
            row = np.empty(cols)
            for j in range(1, cols + 1):
                row[j - 1] = self.get_column(field + "[" + str(i) + "][" + str(j) + "]").get_float(row_index)

            matrix[i - 1] = row

        return matrix

    # Extracts a vector from a category from a specified row_index.
    #
    # _category.matrix[1][1]: v11
    # ....
    # ....
    # _category.matrix[rows][cols]: vRowsCols
    #

    @staticmethod
    def get_vector(self, field: str, rows: int, cols: int, row_index: int) -> np.ndarray:
        vector = np.empty(rows, float)
        for i in range(1, rows + 1):
            vector[i - 1] = self.get_column(field + "[" + str(i) + "]").get_float(row_index)

        return vector
