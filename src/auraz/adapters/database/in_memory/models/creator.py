from dataclasses import dataclass
from datetime import date

from auraz.adapters.database.in_memory.models.attribute import CategoryModel, GenderModel, RegionModel
from auraz.adapters.database.in_memory.models.model import Model
from auraz.adapters.database.in_memory.models.user import UserModel
from auraz.core.domain.entities.creator import Creator, CreatorAttributes, CreatorPersonalInfo
from auraz.core.domain.values.tiktok import TikTokUsername
from auraz.core.domain.values.username import AurazUsername


@dataclass
class CreatorPersonalInfoModel(Model[CreatorPersonalInfo]):
    full_name: str
    birth_date: date

    def to_domain(self) -> CreatorPersonalInfo:
        return CreatorPersonalInfo(**self.__dict__)

    @classmethod
    def from_domain(cls, domain: CreatorPersonalInfo):
        return CreatorPersonalInfoModel(**domain.__dict__)


@dataclass
class CreatorAttributesModel(Model[CreatorAttributes]):
    categories: list[CategoryModel]
    gender: GenderModel
    region: RegionModel

    def to_domain(self) -> CreatorAttributes:
        return CreatorAttributes(
            id=self.id,
            categories=[category.to_domain() for category in self.categories],
            gender=self.gender.to_domain(),
            region=self.region.to_domain(),
        )

    @classmethod
    def from_domain(cls, domain: CreatorAttributes):
        return CreatorAttributesModel(
            id=domain.id,
            categories=[CategoryModel.from_domain(category) for category in domain.categories],
            gender=GenderModel.from_domain(domain.gender),
            region=RegionModel.from_domain(domain.region),
        )


@dataclass
class CreatorModel(Model[Creator]):
    user: UserModel
    username: AurazUsername
    personal_info: CreatorPersonalInfoModel
    attributes: CreatorAttributesModel
    tiktok_username: TikTokUsername

    def to_domain(self) -> Creator:
        return Creator(
            id=self.id,
            user=self.user.to_domain(),
            username=self.username,
            personal_info=self.personal_info.to_domain(),
            attributes=self.attributes.to_domain(),
            tiktok_username=self.tiktok_username,
        )

    @classmethod
    def from_domain(cls, domain: Creator):
        return CreatorModel(
            id=domain.id,
            user=UserModel.from_domain(domain.user),
            username=domain.username,
            personal_info=CreatorPersonalInfoModel.from_domain(domain.personal_info),
            attributes=CreatorAttributesModel.from_domain(domain.attributes),
            tiktok_username=domain.tiktok_username,
        )
