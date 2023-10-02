from typing import NewType, Annotated

from annotated_types import Ge

ID = NewType("ID", Annotated[int, Ge(0)])
