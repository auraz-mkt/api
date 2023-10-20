from http import HTTPStatus

from fastapi import Response

from auraz.adapters.web.cookie import Cookie
from auraz.adapters.web.types.web_code import WebCode
from auraz.adapters.web.types.web_email import WebEmail
from auraz.adapters.web.types.web_exchange import WebExchange
from auraz.core.domain.entities.user import User


class UserResponse(WebExchange):
    webcode: WebCode
    email: WebEmail

    @classmethod
    def create_from(cls, user: User):
        return UserResponse(
            webcode=WebCode.from_id(user.id),
            email=WebEmail.from_auraz_email(user.email),
        )


class CookieResponse(Response):
    @classmethod
    def set(cls, cookie: Cookie):
        response = Response(status_code=HTTPStatus.OK)

        # For more info about cookie options, see:
        # https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies
        # https://fastapi.tiangolo.com/reference/response/#fastapi.Response.set_cookie
        response.set_cookie(
            key=cookie.key,
            value=cookie.value,
            max_age=int(cookie.max_age.total_seconds()),
            expires=str(cookie.expiration),
            samesite=cookie.same_site_policy,
            httponly=cookie.no_javascript_access,
            secure=cookie.mandatory_https_connection,
        )

        return response

    @classmethod
    def delete(cls, cookie: Cookie):
        response = Response(status_code=HTTPStatus.OK)
        response.delete_cookie(cookie.key)
        return response
