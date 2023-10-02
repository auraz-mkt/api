from typing import Generic

from fastapi import APIRouter

from auraz.adapters.web.routers.attributes_dto import AttributesResponse
from auraz.core.domain.entities.attribute import AttributeName, AttributeType
from auraz.ports.database.repository import Repository
from auraz.ports.web.router import Router


class AttributesRouter(Router, Generic[AttributeType]):
    def __init__(
        self,
        name: AttributeName,
        attributes: Repository[AttributeType],
    ):
        self.name = name
        self.attributes = attributes

    def create(self) -> APIRouter:
        router = APIRouter(tags=["Attributes"])

        @router.get(f"/v1/{self.name.plural}", summary=f"List {self.name.plural.capitalize()}")
        async def list_attributes() -> AttributesResponse[AttributeType]:
            attributes = await self.attributes.all()
            return AttributesResponse.create_from(attributes)

        return router
