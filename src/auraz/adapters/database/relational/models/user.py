from sqlalchemy.orm import Mapped, mapped_column

from auraz.adapters.database.relational.models.model import Model
from auraz.core.domain.entities.user import User
from auraz.core.domain.values.email import AurazEmail
from auraz.core.domain.values.password import AurazEncryptedPassword


class UserModel(Model[User]):
    __tablename__ = "users"

    email: Mapped[AurazEmail] = mapped_column("email", unique=True)
    encrypted_password: Mapped[AurazEncryptedPassword] = mapped_column("encrypted_password")

    def to_domain(self) -> User:
        return User(**self.__dict__)

    @classmethod
    def from_domain(cls, domain: User):
        return UserModel(**domain.__dict__)
