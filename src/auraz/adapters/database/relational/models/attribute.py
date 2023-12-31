from abc import abstractmethod
from typing import Generic

from sqlalchemy.orm import Mapped, mapped_column, relationship

from auraz.adapters.database.relational.models.creator import CreatorModel
from auraz.adapters.database.relational.models.model import Model
from auraz.core.domain.entities.attribute import AttributeType, Category, Gender, Region
from auraz.core.domain.values.localized_str import LStr


class AttributeModel(Model[AttributeType], Generic[AttributeType]):
    label: Mapped[LStr] = mapped_column("label", primary_key=True)

    @abstractmethod
    def to_domain(self) -> AttributeType:
        pass

    @classmethod
    @abstractmethod
    def from_domain(cls, domain: AttributeType):
        pass


class CategoryModel(AttributeModel[Category]):
    __tablename__ = "categories"

    creators: Mapped[list[CreatorModel]] = relationship(
        secondary="creators_categories",
        back_populates="categories",
    )

    def to_domain(self) -> Category:
        return Category(**self.__dict__)

    @classmethod
    def from_domain(cls, domain: Category):
        return CategoryModel(**domain.__dict__)


class GenderModel(AttributeModel[Gender]):
    __tablename__ = "genders"

    creators: Mapped[list[CreatorModel]] = relationship(
        back_populates="genders",
    )

    def to_domain(self) -> Gender:
        return Gender(**self.__dict__)

    @classmethod
    def from_domain(cls, domain: Gender):
        return GenderModel(**domain.__dict__)


class RegionModel(AttributeModel[Region]):
    __tablename__ = "regions"

    creators: Mapped[list[CreatorModel]] = relationship(
        back_populates="regions",
    )

    def to_domain(self) -> Region:
        return Region(**self.__dict__)

    @classmethod
    def from_domain(cls, domain: Region):
        return RegionModel(**domain.__dict__)
