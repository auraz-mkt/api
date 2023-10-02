from dataclasses import dataclass

from auraz.core.domain.entities.attribute import Attribute


@dataclass(eq=True, frozen=True)
class Filters:
    categories: list[Attribute]
    genders: list[Attribute]
    regions: list[Attribute]
