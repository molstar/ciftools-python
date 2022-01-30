from __future__ import annotations #supposed to be in python 3.10 but reverted; maybe in python 3.11?

from ...i_cif_data_block import ICIFDataBlock
from ...i_cif_file import ICIFFile


class BinaryCIFFile(ICIFFile):
    @staticmethod
    def from_json(json: str) -> BinaryCIFFile:
        pass

    def to_json(self) -> str:
        pass

    def data_blocks(self) -> ICIFDataBlock:
        pass

