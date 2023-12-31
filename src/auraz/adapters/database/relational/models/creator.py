from datetime import date

from sqlalchemy import Column, Date, ForeignKey, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from auraz.adapters.database.relational.models.attribute import CategoryModel, GenderModel, RegionModel
from auraz.adapters.database.relational.models.model import Model, PrimaryKey
from auraz.adapters.database.relational.models.user import UserModel
from auraz.core.domain.entities.creator import Creator, CreatorAttributes, CreatorPersonalInfo
from auraz.core.domain.values.tiktok import TikTokUsername
from auraz.core.domain.values.username import AurazUsername


class CreatorPersonalInfoModel(Model[CreatorPersonalInfo]):
    __tablename__ = "creator_personal_info"

    id: Mapped[PrimaryKey] = mapped_column(ForeignKey("creators.id"))

    full_name: Mapped[str] = mapped_column(String(256))
    birth_date: Mapped[date] = mapped_column(Date)

    def to_domain(self) -> CreatorPersonalInfo:
        return CreatorPersonalInfo(**self.__dict__)

    @classmethod
    def from_domain(cls, domain: CreatorPersonalInfo):
        return CreatorPersonalInfoModel(**domain.__dict__)


creator_attributes_vs_categories = Table(
    "creator_attributes_vs_categories",
    Model.metadata,
    Column("creator_id", ForeignKey("creators.id"), primary_key=True),
    Column("category_id", ForeignKey("categories.id"), primary_key=True),
)


class CreatorAttributesModel(Model[CreatorAttributes]):
    __tablename__ = "creator_attributes"

    id: Mapped[PrimaryKey] = mapped_column(ForeignKey("creators.id"))

    categories_ids: Mapped[list[PrimaryKey]] = mapped_column(ForeignKey("categories.id"))
    categories: Mapped[list[CategoryModel]] = relationship(
        back_populates="creators",
        secondary="creator_attributes_vs_categories",
    )

    gender_id: Mapped[PrimaryKey] = mapped_column(ForeignKey("genders.id"))
    gender: Mapped[GenderModel] = relationship(back_populates="creators")

    region_id: Mapped[PrimaryKey] = mapped_column(ForeignKey("regions.id"))
    region: Mapped[RegionModel] = relationship(RegionModel, back_populates="creators")

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


class CreatorModel(Model[Creator]):
    __tablename__ = "creators"

    user_id: Mapped[PrimaryKey] = mapped_column("user_id", ForeignKey("users.id"))
    user: Mapped[UserModel] = relationship(uselist=False)

    username: Mapped[AurazUsername] = mapped_column("username")

    personal_info: Mapped[CreatorPersonalInfoModel] = relationship(uselist=False)

    attributes: Mapped[CreatorAttributesModel] = relationship(uselist=False)

    tiktok_username: Mapped[TikTokUsername] = mapped_column("tiktok_username")

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
