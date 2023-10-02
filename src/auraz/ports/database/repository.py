from abc import ABC, abstractmethod
from typing import Any, Generic, Optional

from auraz.core.domain.entities.entity import EntityType
from auraz.core.domain.exception import AurazException
from auraz.core.domain.values.id import ID
from auraz.core.domain.values.localized_str import LStr


class EntityNotFoundByIdException(AurazException):
    def __init__(self, invalid_id: ID):
        self.invalid_id = invalid_id
        super().__init__(
            cause=LStr(
                en_US=f"Invalid identifier `{self.invalid_id}`",
                pt_BR=f"Identificador inválido `{self.invalid_id}`",
            )
        )


class EntityNotFoundByKeyException(Generic[EntityType], AurazException):
    def __init__(self, key: str, invalid_value: Any):
        self.key = key
        self.invalid_value = invalid_value
        super().__init__(
            cause=LStr(
                en_US=f"Invalid value `{self.invalid_value}` for key `{self.key}`",
                pt_BR=f"Valor `{self.invalid_value}` inválido para chave `{self.key}`",
            )
        )


class UnknownFieldException(Generic[EntityType], AurazException):
    def __init__(self, unknown_field: str):
        self.unknown_field = unknown_field
        super().__init__(
            cause=LStr(
                en_US=f"Unknown field `{self.unknown_field}`",
                pt_BR=f"Campo desconhecido `{self.unknown_field}`",
            )
        )


class Repository(ABC, Generic[EntityType]):
    @abstractmethod
    async def all(self) -> list[EntityType]:
        pass

    @abstractmethod
    async def find_all(self, searched_ids: list[ID]) -> list[EntityType]:
        pass

    @abstractmethod
    async def find_some(self, searched_ids: list[ID]) -> list[EntityType]:
        pass

    @abstractmethod
    async def get_by_id(self, searched_id: ID) -> Optional[EntityType]:
        pass

    @abstractmethod
    async def find_by_id(self, searched_id: ID) -> EntityType:
        pass

    @abstractmethod
    async def get_by_key(self, key: str, value: Any) -> Optional[EntityType]:
        pass

    @abstractmethod
    async def find_by_key(self, key: str, value: Any) -> EntityType:
        pass

    @abstractmethod
    async def select(self, field: str, value: Any) -> list[EntityType]:
        pass

    @abstractmethod
    async def create(self, **kwargs) -> EntityType:
        pass

    @abstractmethod
    async def update(self, searched_id: ID, **kwargs) -> EntityType:
        pass
