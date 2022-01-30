from __future__ import annotations  # supposed to be in python 3.10 but reverted; maybe in python 3.11?

from pydantic import BaseModel

from .binary_cif_data_block import BinaryCIFDataBlock
from ...Encoding.encoded_cif_file import EncodedCIFFile
from ...i_cif_data_block import ICIFDataBlock
from ...i_cif_file import ICIFFile


class BinaryCIFFile(ICIFFile, BaseModel):

    def __init__(self, encoded_file: EncodedCIFFile):
        super().__init__()
        self._data_blocks: list[ICIFDataBlock] = []
        for encoded_data_block in encoded_file.data_blocks:
            self._data_blocks.append(BinaryCIFDataBlock(encoded_data_block))

    @staticmethod
    def from_json(json: str) -> BinaryCIFFile:
        return BinaryCIFFile.parse_raw(json)

    def to_json(self) -> str:
        return self.json()

    def data_blocks(self) -> list[ICIFDataBlock]:
        pass
