from .encoded_cif_category import EncodedCIFCategory


class EncodedCIFDataBlock:
    def __init__(self, header: str, categories: list[EncodedCIFCategory]):  # TODO: check use case
        self.header: str = header
        self.categories: list[EncodedCIFCategory] = categories
