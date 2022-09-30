import abc
from dataclasses import dataclass
from typing import Any, List, Optional, Union

import numpy as np
from ciftools.binary.encoding.impl.binary_cif_encoder import BinaryCIFEncoder
from ciftools.cif_format.value_presence import ValuePresenceEnum

@dataclass
class FieldArrays:
    values: Union[np.ndarray, List[str], List[int], List[float]]
    # uint8 array, 0 = defined, 1 = ., 2 = ?
    mask: Optional[np.ndarray] = None

class FieldDesc(abc.ABC):
    name: str

    @abc.abstractmethod
    def create_array(self, total_count: int) -> Union[np.ndarray, list]:
        pass

    @abc.abstractmethod
    def value(self, data: Any, i: int) -> Any:
        pass

    @abc.abstractmethod
    def arrays(self, data: Any) -> Optional[FieldArrays]:
        pass

    @abc.abstractmethod
    def encoder(self, data: Any) -> BinaryCIFEncoder:
        pass

    @abc.abstractmethod
    def presence(self, data: any, i: int) -> ValuePresenceEnum:
        pass

@dataclass
class CategoryDesc:
    name: str
    fields: list[FieldDesc]


@dataclass
class CategoryWriter:
    data: any
    count: int
    desc: CategoryDesc


class CategoryWriterProvider(abc.ABC):
    @abc.abstractmethod
    def category_writer(self, ctx: any) -> CategoryWriter:
        pass


class OutputStream(abc.ABC):
    @abc.abstractmethod
    def write_string(self, data: str) -> bool:
        pass

    @abc.abstractmethod
    def write_binary(self, data: np.ndarray) -> bool:
        pass


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
