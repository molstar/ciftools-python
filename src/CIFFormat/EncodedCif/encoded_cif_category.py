from .encoded_cif_column import EncodedCIFColumn


class EncodedCIFCategory:
    def __init__(self, name: str, row_count: int, columns: list[EncodedCIFColumn]):  # TODO: check use case
        self.name: str = name
        self.rowCount: int = row_count
        self.columns: list[EncodedCIFColumn] = columns
