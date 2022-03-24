import abc

from ciftools.CIFFormat.EncodedCif.encoded_cif_data import EncodedCIFData


class ICIFEncoder(abc.ABC):
    @abc.abstractmethod
    def encode(self, data: object, *args, **kwargs) -> EncodedCIFData:
        pass
