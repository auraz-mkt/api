from dataclasses import dataclass

from auraz.adapters.database.in_memory.internals.storage import Storage
from auraz.core.domain.entities.attribute import Category, Gender, Region
from auraz.core.domain.entities.creator import Creator
from auraz.core.domain.entities.user import User


@dataclass
class Attributes:
    categories: Storage[Category]
    genders: Storage[Gender]
    regions: Storage[Region]


@dataclass
class Database:
    attributes: Attributes
    users: Storage[User]
    creators: Storage[Creator]
