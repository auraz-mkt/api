from dataclasses import dataclass
from typing import TypeVar

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


@dataclass(eq=True, frozen=True)
class Category(Attribute):
    pass


@dataclass(eq=True, frozen=True)
class Gender(Attribute):
    pass


@dataclass(eq=True, frozen=True)
class Region(Attribute):
    pass
