from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from auraz.adapters.database.relational.models.model import Model
from auraz.core.domain.entities.attribute import Category, Gender, Region
from auraz.core.domain.values.localized_str import LStr

# Fix circular import for type checking
# See: https://adamj.eu/tech/2021/05/13/python-type-hints-how-to-fix-circular-imports/
if TYPE_CHECKING:
    from auraz.adapters.database.relational.models.creator import CreatorModel


class CategoryModel(Model[Category]):
    __tablename__ = "categories"

    label: Mapped[LStr] = mapped_column("label", primary_key=True)

    creators: Mapped[list["CreatorModel"]] = relationship(
        secondary="creators_categories",
        back_populates="categories",
    )

    def to_domain(self) -> Category:
        return Category(**self.__dict__)

    @classmethod
    def from_domain(cls, domain: Category):
        return CategoryModel(**domain.__dict__)


class GenderModel(Model[Gender]):
    __tablename__ = "genders"

    label: Mapped[LStr] = mapped_column("label", primary_key=True)

    creators: Mapped[list["CreatorModel"]] = relationship(
        back_populates="genders",
    )

    def to_domain(self) -> Gender:
        return Gender(**self.__dict__)

    @classmethod
    def from_domain(cls, domain: Gender):
        return GenderModel(**domain.__dict__)


class RegionModel(Model[Region]):
    __tablename__ = "regions"

    label: Mapped[LStr] = mapped_column("label", primary_key=True)

    creators: Mapped[list["CreatorModel"]] = relationship(
        back_populates="regions",
    )

    def to_domain(self) -> Region:
        return Region(**self.__dict__)

    @classmethod
    def from_domain(cls, domain: Region):
        return RegionModel(**domain.__dict__)
