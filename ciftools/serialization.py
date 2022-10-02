import msgpack
from ciftools.bin.data import BinaryCIFFile
from ciftools.bin.writer import BinaryCIFWriter
from ciftools.models.data import CIFFile


@staticmethod
def loads(data: bytes, *, lazy: bool = True) -> CIFFile:
    unpacked = msgpack.loads(data)
    return BinaryCIFFile.from_data(unpacked, lazy=lazy)

def create_binary_writer(*, encoder: str = "ciftools-python") -> BinaryCIFWriter:
    return BinaryCIFWriter(encoder=encoder)