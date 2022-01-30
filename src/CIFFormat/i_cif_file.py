import abc

from .i_cif_data_block import ICIFDataBlock
from ..JsonSerialization.i_json_serializable import IJsonSerializable

class ICIFFile(IJsonSerializable, abc.ABC):
    @abc.abstractmethod
    def data_blocks(self) -> ICIFDataBlock:
        pass