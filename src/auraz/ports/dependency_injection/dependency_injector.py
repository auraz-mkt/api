from abc import ABC, abstractmethod
from typing import Generic

from auraz.ports.dependency_injection.types.injectable import InjectableType


class DependencyInjector(ABC, Generic[InjectableType]):
    @abstractmethod
    def build(self) -> InjectableType:
        pass
