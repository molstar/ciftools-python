import abc

from ciftools.Binary.Encoding.types import EncodedCIFData


class CIFEncoderBase(abc.ABC):
    @abc.abstractmethod
    def encode(self, data: object) -> EncodedCIFData:
        pass
