import abc
from optparse import Option

from ciftools.Writer.CategoryWriter import CategoryWriter


class CategoryWriterProvider(abc.ABC):
    @abc.abstractmethod
    def category_writer(self, ctx: Option(object)) -> CategoryWriter:
        pass
