import json
from datetime import date, datetime
from typing import Callable

from auraz.adapters.database.in_memory.internals.database import Attributes, Database
from auraz.adapters.database.in_memory.internals.storage import Storage
from auraz.adapters.database.in_memory.models.attribute import CategoryModel, GenderModel, RegionModel
from auraz.adapters.database.in_memory.models.creator import (
    CreatorAttributesModel,
    CreatorModel,
    CreatorPersonalInfoModel,
)
from auraz.adapters.database.in_memory.models.model import Model, ModelType
from auraz.adapters.database.in_memory.models.user import UserModel
from auraz.core.domain.entities.attribute import Category, Gender, Region
from auraz.core.domain.entities.creator import Creator
from auraz.core.domain.entities.entity import EntityType
from auraz.core.domain.entities.user import User
from auraz.core.domain.values.email import AurazEmail
from auraz.core.domain.values.id import ID
from auraz.core.domain.values.localized_str import LStr
from auraz.core.domain.values.password import AurazEncryptedPassword
from auraz.core.domain.values.tiktok import TikTokUsername
from auraz.core.domain.values.url import URL
from auraz.core.domain.values.username import AurazUsername


class Parser:
    def __init__(self, database_url: URL):
        self.database_file = json.load(open(database_url.path, "r"))

    def parse_database(self) -> Database:
        return Database(
            attributes=self.__parse_attributes(self.database_file["attributes"]),
            users=Storage[User](
                self.__parse_list_into_dict(self.database_file["users"], self.__parse_user),
            ),
            creators=Storage[Creator](
                self.__parse_list_into_dict(self.database_file["creators"], self.__parse_creator),
            ),
        )

    def __parse_attributes(self, data: dict) -> Attributes:
        return Attributes(
            categories=Storage[Category](
                self.__parse_list_into_dict(data["categories"], self.__parse_category),
            ),
            genders=Storage[Gender](
                self.__parse_list_into_dict(data["genders"], self.__parse_gender),
            ),
            regions=Storage[Region](
                self.__parse_list_into_dict(data["regions"], self.__parse_region),
            ),
        )

    def __parse_user(self, data: dict) -> UserModel:
        return UserModel(
            id=data["id"],
            email=self.__parse_auraz_email(data["email"]),
            encrypted_password=self.__parse_auraz_encrypted_password(data["encrypted_password"]),
        )

    def __parse_creator(self, data: dict) -> CreatorModel:
        return CreatorModel(
            id=data["id"],
            user=self.__parse_join_1n(data["user_id"], self.database_file["users"], self.__parse_user),
            username=self.__parse_auraz_username(data["username"]),
            personal_info=self.__parse_creator_personal_info(data["user_id"], data["personal_info"]),
            attributes=self.__parse_creator_attributes(data["user_id"], data["attributes"]),
            tiktok_username=self.__parse_tiktok_username(data["tiktok_username"]),
        )

    def __parse_creator_personal_info(self, user_id: ID, data: dict) -> CreatorPersonalInfoModel:
        return CreatorPersonalInfoModel(
            id=user_id,
            full_name=data["full_name"],
            birth_date=self.__parse_date(data["birth_date"]),
        )

    def __parse_creator_attributes(self, user_id: ID, data: dict) -> CreatorAttributesModel:
        return CreatorAttributesModel(
            id=user_id,
            categories=self.__parse_join_mn(
                data["category_ids"],
                self.database_file["attributes"]["categories"],
                self.__parse_category,
            ),
            gender=self.__parse_join_1n(
                data["gender_id"],
                self.database_file["attributes"]["genders"],
                self.__parse_gender,
            ),
            region=self.__parse_join_1n(
                data["region_id"],
                self.database_file["attributes"]["regions"],
                self.__parse_region,
            ),
        )

    def __parse_gender(self, data: dict) -> GenderModel:
        return GenderModel(id=data["id"], label=self.__parse_lstr(data["label"]))

    def __parse_region(self, data: dict) -> RegionModel:
        return RegionModel(id=data["id"], label=self.__parse_lstr(data["label"]))

    def __parse_category(self, data: dict) -> CategoryModel:
        return CategoryModel(id=data["id"], label=self.__parse_lstr(data["label"]))

    @staticmethod
    def __parse_lstr(data: dict) -> LStr:
        return LStr(pt_BR=data["pt-BR"], en_US=data["en-US"])

    @staticmethod
    def __parse_date(data: str) -> date:
        return datetime.strptime(data, "%Y-%m-%d")

    @staticmethod
    def __parse_url(data: str) -> URL:
        return URL(data)

    @staticmethod
    def __parse_tiktok_username(data: str) -> TikTokUsername:
        return TikTokUsername(data)

    @staticmethod
    def __parse_auraz_email(data: str) -> AurazEmail:
        return AurazEmail(data)

    @staticmethod
    def __parse_auraz_username(data: str) -> AurazUsername:
        return AurazUsername(data)

    @staticmethod
    def __parse_auraz_encrypted_password(data: str) -> AurazEncryptedPassword:
        return AurazEncryptedPassword(data)

    @staticmethod
    def __parse_list_into_dict(
        searched_list: list[dict],
        parse_item: Callable[[dict], Model[EntityType]],
    ) -> dict[ID, Model[EntityType]]:
        return {item.id: item for item in Parser.__parse_list(searched_list, parse_item)}

    @staticmethod
    def __parse_list(
        searched_list: list[dict],
        parse_item: Callable[[dict], Model[EntityType]],
    ) -> list[Model[EntityType]]:
        return [parse_item(item) for item in searched_list]

    @staticmethod
    def __parse_join_mn(
        searched_ids: list[int],
        joined_dict: list[dict],
        parse_item: Callable[[dict], ModelType],
    ) -> list[ModelType]:
        def check_id(item: dict) -> bool:
            return item["id"] in searched_ids

        return [parse_item(item) for item in filter(check_id, joined_dict)]

    @staticmethod
    def __parse_join_1n(
        searched_id: int,
        joined_list: list[dict],
        parse_item: Callable[[dict], ModelType],
    ) -> ModelType:
        def check_id(item: dict) -> bool:
            return item["id"] == searched_id

        return parse_item(next(filter(check_id, joined_list)))
