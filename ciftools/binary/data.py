from typing import Any, Dict, List, Optional, Union

import numpy as np
from ciftools.binary.decoder import decode_cif_data
from ciftools.binary.encoded_data import EncodedCIFCategory, EncodedCIFColumn, EncodedCIFFile
from ciftools.models.data import CIFCategory, CIFColumn, CIFDataBlock, CIFFile, CIFValuePresenceEnum


class BinaryCIFColumn(CIFColumn):
    def __init__(
        self,
        name: str,
        values: np.ndarray,
        value_mask: Union[np.ndarray, None],
    ):
        self.name = name
        self._values = values
        self._value_mask = value_mask
        self._row_count = len(values)

    def get_string(self, row: int) -> str:
        return str(self._values[row])

    def get_integer(self, row: int) -> int:
        return int(self._values[row])

    def get_float(self, row: int) -> float:
        return float(self._values[row])

    def get_value_presence(self, row: int) -> CIFValuePresenceEnum:
        if self._value_mask:
            return self._value_mask[row]
        return 0  # type: ignore

    def are_values_equal(self, row_a: int, row_b: int) -> bool:
        return self._values[row_a] == self._values[row_b]

    def string_equals(self, row: int, value: str) -> bool:
        return str(self._values[row]) == value

    def as_ndarray(
        self, *, dtype: Optional[Union[np.dtype, str]] = None, start: Optional[int] = None, end: Optional[int] = None
    ) -> np.ndarray:
        if dtype is None and start is None and end is None:
            return self._values
        if dtype is None:
            return self._values[start:end]
        return self._values[start:end].astype(dtype)

    def __getitem__(self, idx: Any) -> Any:
        if isinstance(idx, int) and self._value_mask and self._value_mask[idx]:
            return None
        return self._values[idx]

    def __len__(self):
        return self._row_count

    @property
    def value_presences(self) -> Optional[np.ndarray]:
        return self._value_mask


def _decode_cif_column(column: EncodedCIFColumn) -> CIFColumn:
    values = decode_cif_data(column["data"])
    value_mask = decode_cif_data(column["mask"]) if column["mask"] else None
    return BinaryCIFColumn(column["name"], values, value_mask)


class BinaryCIFCategory(CIFCategory):
    def __getitem__(self, name: str) -> BinaryCIFColumn:
        if name not in self._field_cache:
            raise ValueError(f"{name} is not a valid category name")

        if not self._field_cache[name]:
            self._field_cache[name] = _decode_cif_column(self._columns[name])

        return self._field_cache[name]  # type: ignore

    def __contains__(self, key: str):
        return key in self._columns

    def __init__(self, category: EncodedCIFCategory, lazy: bool):
        self._field_names = [c["name"] for c in category["columns"]]
        self._field_cache = {c["name"]: None if lazy else _decode_cif_column(c) for c in category["columns"]}
        self._columns: dict[str, EncodedCIFColumn] = {c["name"]: c for c in category["columns"]}
        self._n_columns = len(category["columns"])
        self._n_rows = category["rowCount"]
        self._name = category["name"][1:]

    @property
    def name(self) -> str:
        return self._name

    @property
    def n_rows(self) -> int:
        return self._n_rows

    @property
    def n_columns(self) -> int:
        return self._n_columns

    @property
    def field_names(self) -> List[str]:
        return self._field_names


class BinaryCIFDataBlock(CIFDataBlock):
    def __getitem__(self, name: str) -> CIFCategory:
        return self._categories[name]

    def __contains__(self, key: str):
        return key in self._categories

    def __init__(self, header: str, categories: Dict[str, BinaryCIFCategory]):
        self._header = header
        self._categories = categories

    @property
    def header(self) -> str:
        return self._header

    @property
    def categories(self) -> Dict[str, CIFCategory]:
        return self._categories  # type: ignore


class BinaryCIFFile(CIFFile):
    def __getitem__(self, index_or_name: Union[int, str]):
        if isinstance(index_or_name, str):
            return self._block_map.get(index_or_name)
        else:
            return (
                self.data_blocks[index_or_name]
                if index_or_name < len(self.data_blocks) and index_or_name >= 0
                else None
            )

    def __len__(self):
        return len(self._data_blocks)

    def __contains__(self, key: str):
        return key in self._block_map

    def __init__(self, data_blocks: List[BinaryCIFDataBlock]):
        self._data_blocks = data_blocks
        self._block_map: dict[str, CIFDataBlock] = {b.header: b for b in data_blocks}

    @staticmethod
    def from_data(data: EncodedCIFFile, *, lazy=True) -> "BinaryCIFFile":
        """
        - lazy:
            - True: individual columns are decoded only when accessed
            - False: decode all columns immediately
        """

        min_version = (0, 3, 0)
        version = tuple(map(int, data["version"].split(".")))
        if version < min_version:
            raise ValueError(f"Invalid version {data['version']}, expected >={'.'.join(map(str, min_version))}")

        data_blocks = [
            BinaryCIFDataBlock(
                block["header"],
                {category["name"][1:]: BinaryCIFCategory(category, lazy) for category in block["categories"]},
            )
            for block in data["dataBlocks"]
        ]

        return BinaryCIFFile(data_blocks)

    @property
    def data_blocks(self) -> List[CIFDataBlock]:
        return self._data_blocks  # type: ignore
