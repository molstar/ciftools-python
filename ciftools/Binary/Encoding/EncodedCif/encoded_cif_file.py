from typing import TypedDict

from .encoded_cif_data_block import EncodedCIFDataBlock


class EncodedCIFFile(TypedDict):
    version: str
    encoder: str
    dataBlocks: list[EncodedCIFDataBlock]
