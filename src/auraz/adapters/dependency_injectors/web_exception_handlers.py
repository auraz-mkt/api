from http import HTTPStatus

from auraz.adapters.integrations.tiktok_scrapper import TikTokPageParsingException
from auraz.adapters.web.authenticator import UnavailableAccessTokenCookieException
from auraz.adapters.web.exception_handlers.base_exception_handler import BaseExceptionHandler
from auraz.adapters.web.types.web_exchange import WebExchangeValidationException
from auraz.core.domain.validation import DomainValidationException
from auraz.core.services.credentials_manager import CredentialsAlreadyExistException, CredentialsUnknownException
from auraz.ports.database.repository import EntityNotFoundByIdException, EntityNotFoundByKeyException
from auraz.ports.dependency_injection.dependency_injector import DependencyInjector
from auraz.ports.dependency_injection.types.web import WebExceptionHandlers
from auraz.ports.security.password_manager import CorruptedPasswordException
from auraz.ports.web.client import ResourceNotRetrievableException


class WebExceptionHandlerDependencyInjector(DependencyInjector[WebExceptionHandlers]):
    def build(self) -> WebExceptionHandlers:
        return WebExceptionHandlers(
            exception_handlers=[
                BaseExceptionHandler(
                    exception_type=CorruptedPasswordException,
                    status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                ),
                BaseExceptionHandler(
                    exception_type=CredentialsAlreadyExistException,
                    status_code=HTTPStatus.CONFLICT,
                ),
                BaseExceptionHandler(
                    exception_type=CredentialsUnknownException,
                    status_code=HTTPStatus.FORBIDDEN,
                ),
                BaseExceptionHandler(
                    exception_type=DomainValidationException,
                    status_code=HTTPStatus.BAD_REQUEST,
                ),
                BaseExceptionHandler(
                    exception_type=EntityNotFoundByIdException,
                    status_code=HTTPStatus.NOT_FOUND,
                    conceal_cause=True,
                ),
                BaseExceptionHandler(
                    exception_type=EntityNotFoundByKeyException,
                    status_code=HTTPStatus.NOT_FOUND,
                    conceal_cause=True,
                ),
                BaseExceptionHandler(
                    exception_type=ResourceNotRetrievableException,
                    status_code=HTTPStatus.NOT_FOUND,
                ),
                BaseExceptionHandler(
                    exception_type=TikTokPageParsingException,
                    status_code=HTTPStatus.BAD_GATEWAY,
                ),
                BaseExceptionHandler(
                    exception_type=UnavailableAccessTokenCookieException,
                    status_code=HTTPStatus.UNAUTHORIZED,
                ),
                BaseExceptionHandler(
                    exception_type=WebExchangeValidationException,
                    status_code=HTTPStatus.BAD_REQUEST,
                ),
            ]
        )
