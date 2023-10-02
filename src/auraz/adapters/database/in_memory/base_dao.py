from dataclasses import fields, replace
from typing import Any, Optional, Type

from auraz.adapters.database.in_memory.internals.storage import Storage
from auraz.adapters.database.in_memory.models.model import Model
from auraz.adapters.database.mapper import mapper
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
        storage: Storage[EntityType],
    ):
        self.item_type = item_type
        self.model_type = model_type
        self.storage = storage

        self.__item_fields = set([field.name for field in fields(self.item_type)])

    @mapper
    async def all(self) -> list[Model[EntityType]]:
        return list(self.storage)

    @mapper
    async def find_all(self, searched_ids: list[ID]) -> list[Model[EntityType]]:
        return [self.storage[searched_id] for searched_id in searched_ids]

    @mapper
    async def find_some(self, searched_ids: list[ID]) -> list[Model[EntityType]]:
        return [model for searched_id in searched_ids if (model := self.storage.get_by_id(searched_id)) is not None]

    @mapper
    async def get_by_id(self, searched_id: ID) -> Optional[Model[EntityType]]:
        return self.storage.get_by_id(searched_id)

    @mapper
    async def find_by_id(self, searched_id: ID) -> Model[EntityType]:
        found_model = await self.get_by_id(searched_id)

        if not found_model:
            raise EntityNotFoundByIdException(invalid_id=searched_id)

        return found_model

    @mapper
    async def get_by_key(self, key: str, value: Any) -> Optional[Model[EntityType]]:
        return self.storage.get_by_key(key, value)

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

        return list(filter(lambda item: getattr(item, field) == value, self.storage))

    @mapper
    async def create(self, **kwargs) -> Model[EntityType]:
        new_item = self.__build_model_from_scratch(**kwargs)

        return self.__save(new_item)

    @mapper
    async def update(self, searched_id: ID, **kwargs) -> Model[EntityType]:
        found_item = self.storage.get_by_id(searched_id)

        if not found_item:
            raise EntityNotFoundByIdException(invalid_id=searched_id)

        updated_item = self.__build_model_from_prototype(found_item, **kwargs)

        return self.__save(updated_item)

    def __build_model_from_scratch(self, **kwargs) -> Model[EntityType]:
        assert self.__check_fields_exist(set(kwargs.keys()))
        new_id = self.storage.generate_id()
        new_item = self.item_type(**kwargs, id=new_id)
        return self.model_type.from_domain(new_item)

    def __build_model_from_prototype(self, original_model: Model[EntityType], **kwargs) -> Model[EntityType]:
        assert self.__check_fields_exist(set(kwargs.keys()))
        return replace(original_model, **kwargs)

    def __check_fields_exist(self, candidate_fields: set[str]) -> bool:
        return candidate_fields.issubset(self.__item_fields)

    def __save(self, model: Model[EntityType]) -> Model[EntityType]:
        self.storage[model.id] = model
        return model
