from auraz.adapters.database.in_memory.base_dao import BaseDAO
from auraz.adapters.database.in_memory.internals.parser import Parser
from auraz.adapters.database.in_memory.models.attribute import CategoryModel, GenderModel, RegionModel
from auraz.adapters.database.in_memory.models.contact import ContactModel
from auraz.adapters.database.in_memory.models.creator import CreatorModel
from auraz.adapters.database.in_memory.models.user import UserModel
from auraz.adapters.settings import Settings
from auraz.core.domain.entities.attribute import Category, Gender, Region
from auraz.core.domain.entities.contact import Contact
from auraz.core.domain.entities.creator import Creator
from auraz.core.domain.entities.user import User
from auraz.ports.dependency_injection.dependency_injector import DependencyInjector
from auraz.ports.dependency_injection.types.database import Repositories


class DatabaseInMemoryDependencyInjector(DependencyInjector[Repositories]):
    def __init__(self, settings: Settings):
        self.database_url = settings.db.url

    def build(self) -> Repositories:
        parser = Parser(database_url=self.database_url)
        database = parser.parse_database()

        return Repositories(
            categories=BaseDAO(
                item_type=Category,
                model_type=CategoryModel,
                storage=database.attributes.categories,
            ),
            genders=BaseDAO(
                item_type=Gender,
                model_type=GenderModel,
                storage=database.attributes.genders,
            ),
            regions=BaseDAO(
                item_type=Region,
                model_type=RegionModel,
                storage=database.attributes.regions,
            ),
            contacts=BaseDAO(
                item_type=Contact,
                model_type=ContactModel,
                storage=database.contacts,
            ),
            users=BaseDAO(
                item_type=User,
                model_type=UserModel,
                storage=database.users,
            ),
            creators=BaseDAO(
                item_type=Creator,
                model_type=CreatorModel,
                storage=database.creators,
            ),
        )
