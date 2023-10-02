from abc import abstractmethod
from dataclasses import dataclass
from typing import Generic

from auraz.adapters.database.in_memory.models.model import Model
from auraz.core.domain.entities.attribute import AttributeType, Category, Gender, Region
from auraz.core.domain.values.localized_str import LStr


@dataclass
class AttributeModel(Model[AttributeType], Generic[AttributeType]):
    label: LStr

    @abstractmethod
    def to_domain(self) -> AttributeType:
        pass

    @classmethod
    @abstractmethod
    def from_domain(cls, domain: AttributeType):
        pass


@dataclass
class CategoryModel(AttributeModel[Category]):
    def to_domain(self) -> Category:
        return Category(**self.__dict__)

    @classmethod
    def from_domain(cls, domain: Category):
        return CategoryModel(**domain.__dict__)


@dataclass
class GenderModel(AttributeModel[Gender]):
    def to_domain(self) -> Gender:
        return Gender(**self.__dict__)

    @classmethod
    def from_domain(cls, domain: Gender):
        return GenderModel(**domain.__dict__)


@dataclass
class RegionModel(AttributeModel[Region]):
    def to_domain(self) -> Region:
        return Region(**self.__dict__)

    @classmethod
    def from_domain(cls, domain: Region):
        return RegionModel(**domain.__dict__)
