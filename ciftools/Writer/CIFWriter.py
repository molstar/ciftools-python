import abc


from ciftools.Writer.CategoryWriterProvider import CategoryWriterProvider
from ciftools.Writer.OutputStream import OutputStream


class CIFWriter(abc.ABC):
    @abc.abstractmethod
    def start_data_block(self, header: str) -> None:
        pass

    @abc.abstractmethod
    def write_category(self, category: CategoryWriterProvider, contexts: [any]) -> None:
        pass

    @abc.abstractmethod
    def encode(self) -> None:
        pass

    @abc.abstractmethod
    def flush(self, stream: OutputStream) -> None:
        pass