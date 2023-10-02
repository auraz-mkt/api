from dataclasses import dataclass
from typing import NewType, TypeVar

from auraz.core.domain.entities.entity import Entity
from auraz.core.domain.values.localized_str import LStr


@dataclass(eq=True, frozen=True)
class Attribute(Entity):
    label: LStr


@dataclass(eq=True, frozen=True)
class AttributeName:
    singular: str
    plural: str


AttributeType = TypeVar("AttributeType", bound=Attribute)

Category = NewType("Category", Attribute)
Gender = NewType("Gender", Attribute)
Region = NewType("Region", Attribute)
