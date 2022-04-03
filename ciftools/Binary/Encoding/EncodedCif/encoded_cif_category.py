from typing import TypedDict

from .encoded_cif_column import EncodedCIFColumn


class EncodedCIFCategory(TypedDict):
    name: str
    rowCount: int
    columns: list[EncodedCIFColumn]
