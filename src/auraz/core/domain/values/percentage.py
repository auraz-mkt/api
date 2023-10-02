from decimal import Decimal
from typing import NewType, Annotated

from annotated_types import Ge, Le

Percentage = NewType("Percentage", Annotated[Decimal, Ge(0), Le(100)])
