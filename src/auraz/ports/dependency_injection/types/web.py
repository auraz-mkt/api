from dataclasses import dataclass

from auraz.ports.dependency_injection.types.injectable import Injectable
from auraz.ports.web.client import Client, HtmlPage
from auraz.ports.web.exception_handler import ExceptionHandler
from auraz.ports.web.router import Router


@dataclass(eq=True, frozen=True)
class WebClients(Injectable):
    html_client: Client[HtmlPage]


@dataclass(eq=True, frozen=True)
class WebExceptionHandlers(Injectable):
    exception_handlers: list[ExceptionHandler]


@dataclass(eq=True, frozen=True)
class WebRouters(Injectable):
    routers: list[Router]
