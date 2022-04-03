import abc

from ciftools.Writer.CategoryWriter import CategoryWriter


class CategoryWriterProvider(abc.ABC):
    @abc.abstractmethod
    def category_writer(self, ctx: any) -> CategoryWriter:
        pass
