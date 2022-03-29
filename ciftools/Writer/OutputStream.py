import abc

import numpy as np


class OutputStream(abc.ABC):
    @abc.abstractmethod
    def write_string(self, data: str) -> bool:
        pass

    @abc.abstractmethod
    def write_binary(self, data: np.ndarray) -> bool:
        pass
