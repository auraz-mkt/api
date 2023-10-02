from dataclasses import dataclass
from typing import TypeVar

from auraz.core.domain.values.id import ID


@dataclass(eq=True, frozen=True)
class Entity:
    id: ID


EntityType = TypeVar("EntityType", bound=Entity)
