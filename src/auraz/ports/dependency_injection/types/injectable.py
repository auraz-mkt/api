from dataclasses import dataclass
from typing import TypeVar


@dataclass(eq=True, frozen=True)
class Injectable:
    pass


InjectableType = TypeVar("InjectableType", bound=Injectable)
