from dataclasses import dataclass

from auraz.adapters.database.in_memory.models.model import Model
from auraz.core.domain.entities.user import User
from auraz.core.domain.values.email import AurazEmail
from auraz.core.domain.values.password import AurazRawPassword


@dataclass
class UserModel(Model[User]):
    email: AurazEmail
    raw_password: AurazRawPassword

    def to_domain(self) -> User:
        return User(**self.__dict__)

    @classmethod
    def from_domain(cls, domain: User):
        return UserModel(**domain.__dict__)
