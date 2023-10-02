from typing import NewType, Annotated

from annotated_types import Ge

Count = NewType("Count", Annotated[int, Ge(0)])
