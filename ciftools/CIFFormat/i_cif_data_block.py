import abc

from ..JsonSerialization.i_json_serializable import IJsonSerializable
from .i_cif_category import ICIFCategory


class ICIFDataBlock(IJsonSerializable, abc.ABC):
    @abc.abstractmethod
    def header(self) -> str:
        pass

    @abc.abstractmethod
    def categories(self) -> dict[str, ICIFCategory]:
        pass

    @abc.abstractmethod
    def get_category(self, name: str) -> ICIFCategory:
        pass

    @abc.abstractmethod
    def additional_data(self) -> dict:
        pass
