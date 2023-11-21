from fastapi import APIRouter

from auraz.adapters.web.routers.contacts_dto import (
    ContactCreationRequest,
    ContactCreationResponse,
    ContactResponse,
    ContactsResponse,
)
from auraz.adapters.web.types.web_code import WebCode
from auraz.core.domain.entities.contact import Contact
from auraz.ports.database.repository import Repository
from auraz.ports.web.router import Router


class ContactsRouter(Router):
    def __init__(self, contacts: Repository[Contact]):
        self.contacts = contacts

    def create(self) -> APIRouter:
        router = APIRouter(tags=["Contacts"])

        @router.get("/v1/contacts")
        async def list_contacts() -> ContactsResponse:
            contacts = await self.contacts.all()
            return ContactsResponse.create_from(contacts)

        @router.get("/v1/contacts/{code}")
        async def show_contact(code: str) -> ContactResponse:
            webcode = WebCode(value=code)
            contact = await self.contacts.find_by_id(webcode.to_id())
            return ContactResponse.create_from(contact)

        @router.post("/v1/contacts")
        async def create_contact(request: ContactCreationRequest) -> ContactCreationResponse:
            new_contact = await self.contacts.create(
                email=request.email.to_auraz_email(),
                type=request.type.to_domain(),
                name=request.name,
                message=request.message,
            )

            new_contact_webcode = WebCode.from_id(new_contact.id)

            return ContactCreationResponse.set(new_contact_webcode)

        return router
