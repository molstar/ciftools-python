from numpy import uint8

from .EEncoding import EEncoding


class EncodedCIFData:
    def __init__(self, encoding: list[EEncoding], data: list[uint8]):  # TODO: check use case
        self.encoding: list[EEncoding] = encoding
        self.data: list[uint8] = data
