from __future__ import annotations  # supposed to be in python 3.10 but reverted; maybe in python 3.11?

from pydantic import BaseModel

from ...Encoding.encoded_cif_category import EncodedCIFCategory
from ...Encoding.encoded_cif_column import EncodedCIFColumn
from ...i_cif_category import ICIFCategory
from ...i_cif_column import ICIFColumn


class BinaryCIFCategory(ICIFCategory, BaseModel):
    var = ('TODO\n'
           '    def __wrapColumn__(self, column: EncodedCIFColumn): Column {\n'
           '        if (!column.data.data) return CIFTools.UndefinedColumn;\n'
           '        let data = decode(column.data);\n'
           '        let mask: Uint8Array | undefined = void 0;\n'
           '        if (column.mask) mask = decode(column.mask);\n'
           '        if (data.buffer && data.byteLength && data.BYTES_PER_ELEMENT) {\n'
           '            return mask ? new MaskedNumericColumn(data, mask) : new NumericColumn(data);\n'
           '        }\n'
           '        return mask ? new MaskedStringColumn(data, mask) : new StringColumn(data);\n'
           '    }\n')

    def __init__(self, encoded_category: EncodedCIFCategory):
        super().__init__()
        self._name: str = encoded_category.name
        self._row_count: int = encoded_category.row_count
        self._column_count: int = len(encoded_category.columns)
        self._column_names: list[str] = []
        self._encoded_columns: dict[str, EncodedCIFColumn] = dict()

        for encoded_column in encoded_category.columns:
            self._column_names.append(encoded_column.name)
            self._encoded_columns[encoded_column.name] = encoded_column

    @staticmethod
    def from_json(json: str) -> BinaryCIFCategory:
        return BinaryCIFCategory.parse_raw(json)

    def to_json(self) -> str:
        return self.json()

    def name(self) -> str:
        pass

    def row_count(self) -> int:
        pass

    def column_count(self) -> int:
        pass

    def column_names(self) -> list[str]:
        pass

    def get_column(self, name: str) -> ICIFColumn:
        pass

    def get_matrix(self, field: str, rows: int, cols: int, row_index: int):
        pass

    def get_vector(self, field: str, rows: int, cols: int, row_index: int) -> list[int]:
        pass
