from dataclasses import dataclass
from enum import Enum

from auraz.core.domain.entities.entity import Entity
from auraz.core.domain.exception import AurazException
from auraz.core.domain.values.email import AurazEmail
from auraz.core.domain.values.localized_str import LStr


class InvalidContactType(AurazException):
    def __init__(self, selector: str):
        super().__init__(
            cause=LStr(
                en_US=f"Invalid contact type: `{selector}`",
                pt_BR=f"Tipo de contato inválido: `{selector}`",
            )
        )


class ContactType(Enum):
    BRAND = LStr(en_US="Brand", pt_BR="Marca")
    CREATOR = LStr(en_US="Creator", pt_BR="Criador")

    @classmethod
    def create_from(cls, selector: str):
        match selector:
            case "creator":
                return ContactType.CREATOR
            case "brand":
                return ContactType.BRAND
            case _:
                raise InvalidContactType(selector)


@dataclass(frozen=True)
class Contact(Entity):
    email: AurazEmail
    type: ContactType
    name: str
    message: str
