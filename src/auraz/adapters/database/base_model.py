from abc import abstractmethod
from dataclasses import dataclass
from typing import Generic

from auraz.core.domain.entities.entity import EntityType


@dataclass
class BaseModel(Generic[EntityType]):
    @abstractmethod
    def to_domain(self) -> EntityType:
        pass

    @classmethod
    @abstractmethod
    def from_domain(cls, domain: EntityType):
        pass
