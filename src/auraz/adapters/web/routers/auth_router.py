from typing import Annotated

from fastapi import APIRouter, Depends

from auraz.adapters.web.authenticator import Authenticator
from auraz.adapters.web.cookie import AccessTokenCookie
from auraz.adapters.web.routers.auth_dto import CookieResponse, UserResponse
from auraz.core.domain.entities.user import Credentials, User
from auraz.core.services.credentials_manager import CredentialsManager
from auraz.ports.web.router import Router


class AuthRouter(Router):
    def __init__(self, authenticator: Authenticator, credentials_manager: CredentialsManager):
        self.authenticator = authenticator
        self.credentials_manager = credentials_manager

    def create(self) -> APIRouter:
        router = APIRouter(tags=["Auth"])
        auth = self.authenticator

        @router.get("/v1/auth/user")
        async def show_user(user: Annotated[User, Depends(auth.retrieve_user)]) -> UserResponse:
            return UserResponse.create_from(user)

        @router.post("/v1/auth/signup")
        async def signup(credentials: Annotated[Credentials, Depends(auth.retrieve_credentials)]) -> CookieResponse:
            new_user = await self.credentials_manager.register_user(credentials)
            cookie = self.authenticator.create_access_token_cookie(new_user)
            return CookieResponse.set(cookie)

        @router.post("/v1/auth/login")
        async def login(credentials: Annotated[Credentials, Depends(auth.retrieve_credentials)]) -> CookieResponse:
            known_user = await self.credentials_manager.search_user(credentials)
            cookie = self.authenticator.create_access_token_cookie(known_user)
            return CookieResponse.set(cookie)

        @router.post("/v1/auth/logout")
        async def logout(
            cookie: Annotated[AccessTokenCookie, Depends(auth.retrieve_access_token_cookie)],
        ) -> CookieResponse:
            return CookieResponse.delete(cookie)

        return router
