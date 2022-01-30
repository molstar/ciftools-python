import abc

from .i_cif_category import ICIFCategory
from ..JsonSerialization.i_json_serializable import IJsonSerializable


class ICIFDataBlock(IJsonSerializable, abc.ABC):
    @abc.abstractmethod
    def header(self) -> str:
        pass

    @abc.abstractmethod
    def categories(self) -> list[ICIFCategory]:
        pass

    @abc.abstractmethod
    def get_category(self, name: str) -> ICIFCategory:
        pass

    @abc.abstractmethod
    def additional_data(self) -> dict:
        pass
