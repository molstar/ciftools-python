from __future__ import annotations  # supposed to be in python 3.10 but reverted; maybe in python 3.11?

import abc


class IJsonSerializable(abc.ABC):
    @abc.abstractmethod
    def to_json(self) -> str:
        pass

    @staticmethod
    @abc.abstractmethod
    def from_json(json: str) -> IJsonSerializable:
        pass
