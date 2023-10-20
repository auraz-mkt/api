from auraz.core.domain.entities.user import Credentials, User
from auraz.core.domain.exception import AurazException
from auraz.core.domain.values.email import AurazEmail
from auraz.core.domain.values.localized_str import LStr
from auraz.ports.database.repository import Repository
from auraz.ports.security.password_manager import PasswordManager


class CredentialsAlreadyExistException(AurazException):
    def __init__(self, candidate_email: AurazEmail):
        super().__init__(
            cause=LStr(
                en_US=f"Email `{candidate_email}` is already registered",
                pt_BR=f"E-mail `{candidate_email}` já está registrado",
            )
        )


class CredentialsUnknownException(AurazException):
    def __init__(self):
        super().__init__(
            cause=LStr(
                en_US="Unknown username or password",
                pt_BR="Nome de usuário ou senha desconhecidos",
            )
        )


class CredentialsManager:
    def __init__(self, users: Repository[User], password_manager: PasswordManager):
        self.users = users
        self.password_manager = password_manager

    async def register_user(self, credentials: Credentials) -> User:
        user = await self.users.get_by_key("email", credentials.email)

        if user:
            raise CredentialsAlreadyExistException(credentials.email)

        new_user = await self.users.create(
            email=credentials.email,
            encrypted_password=self.password_manager.encrypt(credentials.raw_password),
        )

        return new_user

    async def search_user(self, credentials: Credentials) -> User:
        user = await self.users.get_by_key(key="email", value=credentials.email)

        if not user or not self.password_manager.verify(credentials.raw_password, user.encrypted_password):
            raise CredentialsUnknownException()

        return user
