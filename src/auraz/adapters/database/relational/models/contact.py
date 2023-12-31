from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from auraz.adapters.database.relational.models.model import Model
from auraz.core.domain.entities.contact import Contact, ContactType
from auraz.core.domain.values.email import AurazEmail


class ContactModel(Model[Contact]):
    __tablename__ = "contacts"

    email: Mapped[AurazEmail] = mapped_column("email")

    type: Mapped[ContactType] = mapped_column("type")

    name: Mapped[str] = mapped_column("name", String(256))

    message: Mapped[str] = mapped_column("message", String(2048))

    def to_domain(self) -> Contact:
        return Contact(**self.__dict__)

    @classmethod
    def from_domain(cls, domain: Contact):
        return ContactModel(**domain.__dict__)
