from abc import abstractmethod
from dataclasses import dataclass
from typing import Generic, TypeVar

from auraz.adapters.database.base_model import BaseModel
from auraz.core.domain.entities.entity import EntityType
from auraz.core.domain.values.id import ID


@dataclass
class Model(BaseModel, Generic[EntityType]):
    id: ID

    @abstractmethod
    def to_domain(self) -> EntityType:
        pass

    @classmethod
    @abstractmethod
    def from_domain(cls, domain: EntityType):
        pass


ModelType = TypeVar("ModelType", bound=Model)
