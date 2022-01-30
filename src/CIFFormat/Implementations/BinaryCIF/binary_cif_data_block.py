from __future__ import annotations #supposed to be in python 3.10 but reverted; maybe in python 3.11?

from ...i_cif_category import ICIFCategory
from ...i_cif_data_block import ICIFDataBlock


class BinaryCIFDataBlock(ICIFDataBlock):
    @staticmethod
    def from_json(json: str) -> BinaryCIFDataBlock:
        pass

    def to_json(self) -> str:
        pass

    def header(self) -> str:
        pass

    def categories(self) -> [ICIFCategory]:
        pass

    def get_category(self, name: str) -> ICIFCategory:
        pass

    def additional_data(self) -> dict:
        pass




