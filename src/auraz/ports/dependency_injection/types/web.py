from dataclasses import dataclass

from auraz.ports.web.client import HtmlPage, Client
from auraz.ports.web.exception_handler import ExceptionHandler
from auraz.ports.web.router import Router


@dataclass(eq=True, frozen=True)
class WebClients:
    html_client: Client[HtmlPage]


@dataclass(eq=True, frozen=True)
class WebExceptionHandlers:
    exception_handlers: list[ExceptionHandler]


@dataclass(eq=True, frozen=True)
class WebRouters:
    routers: list[Router]
