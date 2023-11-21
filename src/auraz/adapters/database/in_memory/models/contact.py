from dataclasses import dataclass

from auraz.core.domain.entities.contact import Contact, ContactType

from auraz.adapters.database.in_memory.models.model import Model
from auraz.core.domain.values.email import AurazEmail


@dataclass
class ContactModel(Model[Contact]):
    email: AurazEmail
    type: ContactType
    name: str
    message: str

    def to_domain(self) -> Contact:
        return Contact(**self.__dict__)

    @classmethod
    def from_domain(cls, domain: Contact):
        return ContactModel(**domain.__dict__)
