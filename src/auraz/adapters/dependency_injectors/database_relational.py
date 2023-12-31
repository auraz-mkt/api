from sqlalchemy import create_engine

from auraz.adapters.database.relational.base_dao import BaseDAO
from auraz.adapters.database.relational.models.attribute import CategoryModel, GenderModel, RegionModel
from auraz.adapters.database.relational.models.contact import ContactModel
from auraz.adapters.database.relational.models.creator import CreatorModel
from auraz.adapters.database.relational.models.user import UserModel
from auraz.core.domain.entities.attribute import Category, Gender, Region
from auraz.core.domain.entities.contact import Contact
from auraz.core.domain.entities.creator import Creator
from auraz.core.domain.entities.user import User
from auraz.core.domain.values.url import URL
from auraz.ports.dependency_injection.dependency_injector import DependencyInjector
from auraz.ports.dependency_injection.types.database import Repositories


class DatabaseRelationalDependencyInjector(DependencyInjector):
    def __init__(self, database_url: URL):
        self.database_url = database_url
        self.engine = create_engine(str(database_url))

    def build(self) -> Repositories:
        return Repositories(
            categories=BaseDAO(
                item_type=Category,
                model_type=CategoryModel,
                engine=self.engine,
            ),
            genders=BaseDAO(
                item_type=Gender,
                model_type=GenderModel,
                engine=self.engine,
            ),
            regions=BaseDAO(
                item_type=Region,
                model_type=RegionModel,
                engine=self.engine,
            ),
            contacts=BaseDAO(
                item_type=Contact,
                model_type=ContactModel,
                engine=self.engine,
            ),
            users=BaseDAO(
                item_type=User,
                model_type=UserModel,
                engine=self.engine,
            ),
            creators=BaseDAO(
                item_type=Creator,
                model_type=CreatorModel,
                engine=self.engine,
            ),
        )
