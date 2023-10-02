from auraz.adapters.database.base_model import BaseModel
from auraz.core.domain.entities.entity import EntityType


def mapper(func):
    async def wrapper(*args, **kwargs) -> list[EntityType] | EntityType | None:
        output = await func(*args, **kwargs)

        if output is None:
            return None
        if isinstance(output, list):
            return _convert_multiple(output)
        return _convert_single(output)

    return wrapper


def _convert_multiple(elements: list[EntityType] | list[BaseModel[EntityType]]) -> list[EntityType]:
    return [_convert_single(element) for element in elements]


def _convert_single(elements: EntityType | BaseModel[EntityType]) -> EntityType:
    return elements.to_domain() if isinstance(elements, BaseModel) else elements
