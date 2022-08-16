import abc
from ciftools.binary.encoding.types import EncodedCIFData


class BinaryCIFEncoderBase(abc.ABC):
    @abc.abstractmethod
    def encode_cif_data(self, data: any) -> EncodedCIFData:
        pass

