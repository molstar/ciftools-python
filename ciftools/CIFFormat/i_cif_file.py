from __future__ import annotations  # supposed to be in python 3.10 but reverted; maybe in python 3.11?

import abc

from .i_cif_data_block import ICIFDataBlock
from ..JsonSerialization.i_json_serializable import IJsonSerializable


class ICIFFile(IJsonSerializable, abc.ABC):
    @abc.abstractmethod
    def data_blocks(self) -> ICIFDataBlock:
        pass
