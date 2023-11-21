from enum import Enum
from http import HTTPStatus

from fastapi import Response

from auraz.adapters.web.types.web_code import WebCode
from auraz.adapters.web.types.web_email import WebEmail
from auraz.adapters.web.types.web_exchange import WebExchange
from auraz.core.domain.entities.contact import Contact, ContactType


class ContactTypeRequest(Enum):
    BRAND = "brand"
    CREATOR = "creator"

    def to_domain(self) -> ContactType:
        return ContactType.create_from(self.value)


class ContactCreationRequest(WebExchange):
    email: WebEmail
    type: ContactTypeRequest
    name: str
    message: str


class ContactResponse(WebExchange):
    webcode: WebCode
    name: str
    message: str

    @classmethod
    def create_from(cls, contact: Contact):
        return ContactResponse(
            webcode=WebCode.from_id(contact.id),
            name=contact.name,
            message=contact.message,
        )


class ContactsResponse(WebExchange):
    data: list[ContactResponse]

    @classmethod
    def create_from(cls, contacts: list[Contact]):
        return ContactsResponse(data=list(map(ContactResponse.create_from, contacts)))


class ContactCreationResponse(Response):
    @classmethod
    def set(cls, new_contact_webcode: WebCode):
        response = ContactCreationResponse(status_code=HTTPStatus.CREATED)
        response.headers["Location"] = f"/v1/contacts/{new_contact_webcode}"
        return response
