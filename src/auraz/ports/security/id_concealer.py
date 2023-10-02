from abc import ABC, abstractmethod
from typing import Annotated, NewType

from annotated_types import Gt

from auraz.core.domain.values.id import ID

Code = NewType("Code", str)
CodeLength = NewType("CodeLength", Annotated[int, Gt(0)])


class IdConcealer(ABC):
    @property
    @abstractmethod
    def min_code_length(self) -> CodeLength:
        pass

    @abstractmethod
    def encode(self, identifier: ID) -> Code:
        pass

    @abstractmethod
    def decode(self, code: Code) -> ID:
        pass


"""
Singleton IdConcealer to be used for other modules
"""
__instance: IdConcealer


def initialize(id_concealer: IdConcealer):
    """
    Initialize id_concealer singleton
    """
    global __instance
    __instance = id_concealer


def get() -> IdConcealer:
    """
    Retrieve id_concealer singleton
    """
    global __instance
    assert __instance is not None
    return __instance
