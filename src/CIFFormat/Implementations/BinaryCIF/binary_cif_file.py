from __future__ import annotations #supposed to be in python 3.10 but reverted; maybe in python 3.11?

from pydantic import BaseModel

from ...i_cif_data_block import ICIFDataBlock
from ...i_cif_file import ICIFFile


class BinaryCIFFile(ICIFFile, BaseModel):
    @staticmethod
    def from_json(json: str) -> BinaryCIFFile:
        return BinaryCIFFile.parse_raw(json)

    def to_json(self) -> str:
        return self.json()

    def data_blocks(self) -> ICIFDataBlock:
        pass

