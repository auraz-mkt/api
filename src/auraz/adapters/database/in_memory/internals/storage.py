from typing import Any, Generic, Optional

from auraz.adapters.database.in_memory.models.model import Model
from auraz.core.domain.entities.entity import EntityType
from auraz.core.domain.values.id import ID


class Storage(Generic[EntityType]):
    def __init__(self, data: dict[ID, Model[EntityType]]):
        self.__data = data
        self.__max_id = max(self.__data.keys())

    def __iter__(self):
        return iter(self.__data.values())

    def __getitem__(self, data_id: ID) -> Model[EntityType]:
        return self.__data[data_id]

    def __setitem__(self, data_id: ID, model: Model[EntityType]):
        self.__data[data_id] = model

    def get_by_id(self, data_id: ID) -> Optional[Model[EntityType]]:
        return self.__data.get(data_id)

    def get_by_key(self, key: str, value: Any) -> Optional[Model[EntityType]]:
        return next(filter(lambda model: getattr(model, key) == value, self), None)

    def generate_id(self) -> ID:
        next_id = ID(self.__max_id + 1)
        self.__max_id = next_id
        return next_id
