import abc

from ciftools.writer.CategoryWriterProvider import CategoryWriterProvider
from ciftools.writer.OutputStream import OutputStream


class CIFWriter(abc.ABC):
    @abc.abstractmethod
    def start_data_block(self, header: str) -> None:
        pass

    @abc.abstractmethod
    def write_category(self, category: CategoryWriterProvider, contexts: list) -> None:
        pass

    @abc.abstractmethod
    def encode(self) -> None:
        pass

    @abc.abstractmethod
    def flush(self, stream: OutputStream) -> None:
        pass
