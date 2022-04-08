from typing import Optional, TypedDict

from .encoded_cif_data import EncodedCIFData


class EncodedCIFColumn(TypedDict):
    name: str
    data: EncodedCIFData
    mask: Optional[EncodedCIFData]
