import abc

from ciftools.Binary.Encoding.EncodedCif.encoded_cif_data import EncodedCIFData


class ICIFEncoder(abc.ABC):
    @abc.abstractmethod
    def encode(self, data: object) -> EncodedCIFData:
        pass
