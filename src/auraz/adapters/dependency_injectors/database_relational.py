from sqlalchemy import create_engine

from auraz.adapters.database.relational.base_dao import BaseDAO
from auraz.adapters.database.relational.models.attribute import CategoryModel, GenderModel, RegionModel
from auraz.adapters.database.relational.models.contact import ContactModel
from auraz.adapters.database.relational.models.creator import CreatorModel
from auraz.adapters.database.relational.models.user import UserModel
from auraz.adapters.settings import Settings
from auraz.core.domain.entities.attribute import Category, Gender, Region
from auraz.core.domain.entities.contact import Contact
from auraz.core.domain.entities.creator import Creator
from auraz.core.domain.entities.user import User
from auraz.ports.dependency_injection.dependency_injector import DependencyInjector
from auraz.ports.dependency_injection.types.database import Repositories


class DatabaseRelationalDependencyInjector(DependencyInjector[Repositories]):
    def __init__(self, settings: Settings):
        self.database_url = settings.db.url

    def build(self) -> Repositories:
        engine = create_engine(str(self.database_url))

        return Repositories(
            categories=BaseDAO(
                item_type=Category,
                model_type=CategoryModel,
                engine=engine,
            ),
            genders=BaseDAO(
                item_type=Gender,
                model_type=GenderModel,
                engine=engine,
            ),
            regions=BaseDAO(
                item_type=Region,
                model_type=RegionModel,
                engine=engine,
            ),
            contacts=BaseDAO(
                item_type=Contact,
                model_type=ContactModel,
                engine=engine,
            ),
            users=BaseDAO(
                item_type=User,
                model_type=UserModel,
                engine=engine,
            ),
            creators=BaseDAO(
                item_type=Creator,
                model_type=CreatorModel,
                engine=engine,
            ),
        )
