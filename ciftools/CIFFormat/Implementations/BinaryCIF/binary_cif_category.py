from __future__ import annotations  # supposed to be in python 3.10 but reverted; maybe in python 3.11?

from ciftools.Binary.Decoder import decode_cif_column
from ciftools.Binary.Encoding.EncodedCif.encoded_cif_category import EncodedCIFCategory
from ciftools.Binary.Encoding.EncodedCif.encoded_cif_column import EncodedCIFColumn
from ciftools.CIFFormat.i_cif_category import ICIFCategory
from ciftools.CIFFormat.i_cif_column import ICIFColumn
from ciftools.CIFFormat.Implementations.BinaryCIF.binary_cif_column import BinaryCIFColumn
from ciftools.CIFFormat.Implementations.BinaryCIF.ColumnTypes.undefined_cif_column import UndefinedCIFColumn


class BinaryCIFCategory(ICIFCategory):
    __undefined_column__ = UndefinedCIFColumn()

    def __getattr__(self, name: str) -> object:
        return self[name]

    def __getitem__(self, name: str) -> BinaryCIFColumn:
        if name not in self._field_cache:
            return None

        if not self._field_cache[name]:
            self._field_cache[name] = decode_cif_column(self._columns[name])

        return self._field_cache[name]

    def __contains__(self, key: str):
        return key in self._columns

    def __init__(self, category: EncodedCIFCategory, lazy: bool):
        self.field_names = [c["name"] for c in category["columns"]]
        self._field_cache = {c["name"]: None if lazy else decode_cif_column(c) for c in category["columns"]}
        self._columns: dict[str, EncodedCIFColumn] = {c["name"]: c for c in category["columns"]}
        self.row_count = category["rowCount"]
        self.name = category["name"][1:]

    @staticmethod
    def from_json(json: str) -> BinaryCIFCategory:
        return BinaryCIFCategory.parse_raw(json)

    def to_json(self) -> str:
        return self.json()

    def name(self) -> str:
        return self._name

    def row_count(self) -> int:
        return self._row_count

    def column_count(self) -> int:
        return self._column_count

    def column_names(self) -> list[str]:
        return self.field_names

    def get_column(self, name: str) -> ICIFColumn:
        encoded_cif_column = self._columns.get(name, None)
        if encoded_cif_column is not None:
            return BinaryCIFCategory.__wrap_column__(encoded_cif_column)

        return BinaryCIFCategory.__undefined_column__

    @staticmethod
    def __wrap_column__(encoded_cif_column: EncodedCIFColumn) -> ICIFColumn:
        if encoded_cif_column["data"]["data"] is None:
            return BinaryCIFCategory.__undefined_column__

        return decode_cif_column(encoded_cif_column)


"""
        data = decode_cif_data(encoded_cif_column.data)
        mask: list[uint8] = None

        if encoded_cif_column.mask is not None:
            mask = decode_cif_data(encoded_cif_column.mask)

        if data.buffer is not None and data.byteLength is not None and data.BYTES_PER_ELEMENT is not None:
            if mask is None:
                return NumericColumn(data)

            return MaskedNumericColumn(data, mask)

        if mask is None:
            return StringColumn(data)

        return MaskedStringColumn(data, mask)
"""
