from abc import abstractmethod
from typing import Annotated, Generic, TypeVar

from sqlalchemy import Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from auraz.adapters.database.base_model import BaseModel
from auraz.core.domain.entities.contact import ContactType
from auraz.core.domain.entities.entity import EntityType
from auraz.core.domain.values.count import Count
from auraz.core.domain.values.email import AurazEmail
from auraz.core.domain.values.id import ID
from auraz.core.domain.values.localized_str import LStr
from auraz.core.domain.values.password import AurazEncryptedPassword
from auraz.core.domain.values.tiktok import TikTokUsername
from auraz.core.domain.values.url import URL
from auraz.core.domain.values.username import AurazUsername

PrimaryKey = Annotated[ID, mapped_column(primary_key=True)]


class Model(DeclarativeBase, BaseModel, Generic[EntityType]):
    type_annotation_map = {
        Count: Integer(),
        ID: Integer(),
        URL: String(256),
        ContactType: String(32),
        AurazEmail: String(128),
        AurazEncryptedPassword: String(128),
        AurazUsername: String(128),
        TikTokUsername: String(128),
        LStr: JSONB,
    }

    id: Mapped[PrimaryKey] = mapped_column("id")

    @abstractmethod
    def to_domain(self) -> EntityType:
        pass

    @classmethod
    @abstractmethod
    def from_domain(cls, domain: EntityType):
        pass


ModelType = TypeVar("ModelType", bound=Model)
