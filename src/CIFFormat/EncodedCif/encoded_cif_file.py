from .encoded_cif_data_block import EncodedCIFDataBlock


class EncodedCIFFile:
    def __init__(self, version: str, encoder: str, data_blocks: list[EncodedCIFDataBlock]):  # TODO: check use case
        self.version: str = version
        self.encoder: str = encoder
        self.dataBlocks: list[EncodedCIFDataBlock] = data_blocks


