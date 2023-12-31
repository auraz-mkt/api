from dataclasses import fields, replace
from typing import Any, Optional, Type, cast

from sqlalchemy import ColumnElement, Engine, Executable, select
from sqlalchemy.orm import Session

from auraz.adapters.database.mapper import mapper
from auraz.adapters.database.relational.internals.transaction import transaction
from auraz.adapters.database.relational.models.model import Model
from auraz.core.domain.entities.entity import EntityType
from auraz.core.domain.values.id import ID
from auraz.ports.database.repository import (
    EntityNotFoundByIdException,
    EntityNotFoundByKeyException,
    Repository,
    UnknownFieldException,
)


class BaseDAO(Repository[EntityType]):
    def __init__(
        self,
        item_type: Type[EntityType],
        model_type: Type[Model[EntityType]],
        engine: Engine,
    ):
        self.item_type = item_type
        self.model_type = model_type
        self.engine = engine

        self.__item_fields = set(field.name for field in fields(self.model_type))

    @mapper
    async def all(self) -> list[Model[EntityType]]:
        sql = select(self.model_type)
        return self.__fetch_all(sql)

    @mapper
    async def find_all(self, searched_ids: list[ID]) -> list[Model[EntityType]]:
        sql = select(self.model_type).where(self.model_type.id.in_(searched_ids))
        return self.__fetch_all(sql)

    @mapper
    async def find_some(self, searched_ids: list[ID]) -> list[Model[EntityType]]:
        sql = select(self.model_type).where(self.model_type.id.in_(searched_ids))
        return self.__fetch_all(sql)

    @mapper
    async def get_by_id(self, searched_id: ID) -> Optional[Model[EntityType]]:
        sql = select(self.model_type).where(self.model_type.id == searched_id)
        return self.__fetch_one(sql)

    @mapper
    async def find_by_id(self, searched_id: ID) -> Model[EntityType]:
        found_model = await self.get_by_id(searched_id)

        if not found_model:
            raise EntityNotFoundByIdException(invalid_id=searched_id)

        return found_model

    @mapper
    async def get_by_key(self, key: str, value: Any) -> Optional[Model[EntityType]]:
        sql = select(self.model_type).where(cast(ColumnElement[bool], getattr(self.model_type, key) == value))
        return self.__fetch_one(sql)

    @mapper
    async def find_by_key(self, key: str, value: Any) -> Model[EntityType]:
        found_model = await self.get_by_key(key, value)

        if not found_model:
            raise EntityNotFoundByKeyException(key=key, invalid_value=value)

        return found_model

    @mapper
    async def select(self, field: str, value: Any) -> list[Model[EntityType]]:
        if not self.__check_fields_exist(set(field)):
            raise UnknownFieldException(unknown_field=field)

        sql = select(self.model_type).where(cast(ColumnElement[bool], getattr(self.model_type, field) == value))
        return self.__fetch_all(sql)

    @mapper
    async def create(self, **kwargs) -> Model[EntityType]:
        new_item = self.__build_model_from_scratch(**kwargs)

        return self.__save(new_item)

    @mapper
    async def update(self, searched_id: ID, **kwargs) -> Model[EntityType]:
        found_item = await self.get_by_id(searched_id)

        if not found_item:
            raise EntityNotFoundByIdException(invalid_id=searched_id)

        updated_item = self.__build_model_from_prototype(found_item, **kwargs)

        return self.__save(updated_item)

    def __build_model_from_scratch(self, **kwargs) -> Model[EntityType]:
        assert self.__check_fields_exist(set(kwargs.keys()))
        return self.model_type(**kwargs)

    def __build_model_from_prototype(self, original_model: Model[EntityType], **kwargs) -> Model[EntityType]:
        assert self.__check_fields_exist(set(kwargs.keys()))
        return replace(original_model, **kwargs)

    def __check_fields_exist(self, candidate_fields: set[str]) -> bool:
        return candidate_fields.issubset(self.__item_fields)

    @staticmethod
    @transaction
    def __fetch_one(session: Session, sql: Executable) -> Optional[Model[EntityType]]:
        row = session.execute(sql).fetchone()
        return row[0] if row else None

    @staticmethod
    @transaction
    def __fetch_all(session: Session, sql: Executable) -> list[Model[EntityType]]:
        rows = session.execute(sql).fetchall()
        return [row[0] for row in rows]

    @staticmethod
    @transaction
    def __save(session: Session, model: Model[EntityType]) -> Model[EntityType]:
        session.add(model)
        return model
