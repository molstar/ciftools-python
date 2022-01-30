from __future__ import annotations  # supposed to be in python 3.10 but reverted; maybe in python 3.11?

from pydantic import BaseModel

from .binary_cif_category import BinaryCIFCategory
from ...Encoding.encoded_cif_data_block import EncodedCIFDataBlock
from ...i_cif_category import ICIFCategory
from ...i_cif_data_block import ICIFDataBlock


class BinaryCIFDataBlock(ICIFDataBlock, BaseModel):

    def __init__(self, encoded_data_block: EncodedCIFDataBlock):
        super().__init__()
        self._header: str = encoded_data_block.header
        self._categories: list[BinaryCIFCategory] = []
        self._category_map: dict[str, BinaryCIFCategory] = dict()
        for encoded_category in encoded_data_block.categories:
            category = BinaryCIFCategory(encoded_category)
            self._categories.append(category)
            self._category_map[category.name()] = category

    @staticmethod
    def from_json(json: str) -> BinaryCIFDataBlock:
        return BinaryCIFDataBlock.parse_raw(json)

    def to_json(self) -> str:
        return self.json()

    def header(self) -> str:
        pass

    def categories(self) -> list[ICIFCategory]:
        pass

    def get_category(self, name: str) -> ICIFCategory:
        pass

    def additional_data(self) -> dict:
        pass




