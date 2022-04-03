from typing import TypedDict

from .encoded_cif_category import EncodedCIFCategory


class EncodedCIFDataBlock(TypedDict):
    header: str
    categories: list[EncodedCIFCategory]
