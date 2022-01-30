from .encoded_cif_data import EncodedCIFData


class EncodedCIFColumn:
    def __init__(self, name: str, data: EncodedCIFData, mask: EncodedCIFData | None):  # TODO: check use case
        self.name: str = name
        self.data: EncodedCIFData = data
        self.mask: EncodedCIFData | None = mask
