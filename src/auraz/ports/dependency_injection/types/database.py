from dataclasses import dataclass

from auraz.core.domain.entities.attribute import Category, Gender, Region
from auraz.core.domain.entities.contact import Contact
from auraz.core.domain.entities.creator import Creator
from auraz.core.domain.entities.user import User
from auraz.ports.database.repository import Repository
from auraz.ports.dependency_injection.types.injectable import Injectable


@dataclass(eq=True, frozen=True)
class Repositories(Injectable):
    categories: Repository[Category]
    genders: Repository[Gender]
    regions: Repository[Region]
    contacts: Repository[Contact]
    users: Repository[User]
    creators: Repository[Creator]
