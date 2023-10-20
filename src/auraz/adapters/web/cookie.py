from dataclasses import dataclass
from typing import Literal

from fastapi import Response

from auraz.adapters.web.types.web_code import WebCode
from auraz.ports.security.access_token import Expiration, JWT, MaxAge


@dataclass
class Cookie:
    key: str
    value: str
    max_age: MaxAge
    expiration: Expiration
    no_javascript_access: bool
    restricts_same_origin: bool
    mandatory_https_connection: bool

    @property
    def same_site_policy(self) -> Literal["strict", "lax"]:
        if self.restricts_same_origin:
            return "strict"
        return "lax"

    def set(self, response: Response):
        # For more info about cookie options, see:
        # https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies
        # https://fastapi.tiangolo.com/reference/response/#fastapi.Response.set_cookie
        response.set_cookie(
            key=self.key,
            value=self.value,
            max_age=int(self.max_age.total_seconds()),
            expires=str(self.expiration),
            samesite=self.same_site_policy,
            httponly=self.no_javascript_access,
            secure=self.mandatory_https_connection,
        )

    def delete(self, response: Response):
        response.delete_cookie(self.key)


@dataclass
class AccessTokenCookie(Cookie):
    owner: WebCode

    @classmethod
    def create_from(cls, owner: WebCode, access_token: JWT, max_age: MaxAge, expiration: Expiration):
        return AccessTokenCookie(
            owner=owner,
            key="access_token",
            value=str(access_token),
            max_age=max_age,
            expiration=expiration,
            no_javascript_access=True,
            restricts_same_origin=False,
            mandatory_https_connection=True,
        )
