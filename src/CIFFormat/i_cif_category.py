import abc

from .i_cif_column import ICIFColumn
from ..JsonSerialization.i_json_serializable import IJsonSerializable

class ICIFCategory(abc.ABC, IJsonSerializable):
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
    def column_names(self) -> [str]:
        pass

    @abc.abstractmethod
    def get_column(self, name: str) -> ICIFColumn:
        pass


    # Extracts a  matrix from a category from a specified row_index.
    #
    # _category.matrix[1][1]: v11
    # ....
    # ....
    # _category.matrix[rows][cols]: vRowsCols
    #
    @abc.abstractmethod
    def get_matrix(self, field: str, rows: int, cols: int, row_index: int):
        pass

    # Extracts a vector from a category from a specified row_index.
    #
    # _category.matrix[1][1]: v11
    # ....
    # ....
    # _category.matrix[rows][cols]: vRowsCols
    #
    @abc.abstractmethod
    def get_vector(self, field: str, rows: int, cols: int, row_index: int) -> [int]:
        pass