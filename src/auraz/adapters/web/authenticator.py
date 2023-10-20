from datetime import timedelta
from typing import Annotated

from fastapi import Depends, Form, Request
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security import OAuth2

from auraz.adapters.web.cookie import AccessTokenCookie
from auraz.adapters.web.types.web_code import WebCode
from auraz.adapters.web.types.web_email import WebEmail
from auraz.adapters.web.types.web_password import WebPassword
from auraz.core.domain.entities.user import Credentials, User
from auraz.core.domain.exception import AurazException
from auraz.core.domain.values.localized_str import LStr
from auraz.ports.database.repository import Repository
from auraz.ports.security.access_token import AccessToken, JWT, MaxAge

DEFAULT_MAX_AGE = MaxAge(timedelta(hours=12))


class UnavailableAccessTokenCookieException(AurazException):
    def __init__(self):
        super().__init__(
            cause=LStr(
                en_US="Request did not provide `access_token` cookie",
                pt_BR="Requisição não proveu o cookie `access_token`",
            )
        )


class OAuth2CredentialsForm:
    """
    Based on fastapi.security.oauth2.OAuth2PasswordRequestForm

    `username` and `password` are the default form fields according to the OAuth2 protocol.
    Although creators and brands will have an Auraz username, the identifier for auth purposes
    will be the user's email.
    """

    def __init__(
        self,
        username: Annotated[WebEmail, Form()],
        password: Annotated[WebPassword, Form()],
        scope: Annotated[str, Form()] = "",
    ):
        self.username = username
        self.password = password
        self.scopes = scope.split()


class OAuth2PasswordBearerWithAccessTokenCookie(OAuth2):
    """
    Based on fastapi.security.oauth2.OAuth2PasswordBearer
    """

    def __init__(
        self,
        token_url: str,
        scopes: dict[str, str],
    ):
        flows = OAuthFlowsModel(password={"tokenUrl": token_url, "scopes": scopes})
        super().__init__(
            flows=flows,
            scheme_name=self.__class__.__name__,
            description="HTTP-only `access_token` cookie",
        )

    async def __call__(self, request: Request) -> JWT:
        # Get JWT token from HTTP-only `access_token` cookie
        access_token = request.cookies.get("access_token")

        if not access_token:
            raise UnavailableAccessTokenCookieException()

        return JWT(access_token)


class Authenticator:
    oauth2_scheme = OAuth2PasswordBearerWithAccessTokenCookie(token_url="/v1/login", scopes={})

    def __init__(self, users: Repository[User], access_token: AccessToken):
        self.users = users
        self.access_token = access_token

    @staticmethod
    def retrieve_credentials(form_data: Annotated[OAuth2CredentialsForm, Depends()]) -> Credentials:
        return Credentials(
            email=form_data.username.to_auraz_email(),
            raw_password=form_data.password.to_auraz_raw_password(),
        )

    def retrieve_access_token_cookie(self, access_token: Annotated[JWT, Depends(oauth2_scheme)]) -> AccessTokenCookie:
        subject, max_age, expiration = self.access_token.decode(access_token)
        user = WebCode.from_subject(subject)
        return AccessTokenCookie.create_from(user, access_token, max_age, expiration)

    async def retrieve_user(self, access_token: Annotated[JWT, Depends(oauth2_scheme)]) -> User:
        subject, max_age, expiration = self.access_token.decode(access_token)
        user_id = WebCode.from_subject(subject).to_id()
        return await self.users.find_by_id(user_id)

    def create_access_token_cookie(self, user: User) -> AccessTokenCookie:
        user_webcode = WebCode.from_id(user.id)
        subject = user_webcode.to_subject()
        max_age = DEFAULT_MAX_AGE

        access_token, expiration = self.access_token.encode(subject=subject, max_age=max_age)
        return AccessTokenCookie.create_from(user_webcode, access_token, max_age, expiration)
