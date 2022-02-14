from typing import TypedDict

from numpy import uint8

from ...Binary.Encoding import EEncoding, EncodingBase


class EncodedCIFData(TypedDict):
    def __init__(self, encoding: list[EncodingBase], data: bytes):  # TODO: check use case
        self.encoding: list[EncodingBase] = encoding
        self.data: bytes = data
