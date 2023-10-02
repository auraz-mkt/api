import aiohttp

from auraz.adapters.web.clients.base_aiohttp_client import BaseAioHttpClient
from auraz.ports.dependency_injection.dependency_injector import DependencyInjector
from auraz.ports.dependency_injection.types.web import WebClients
from auraz.ports.web.client import HtmlPage


class WebClientsDependencyInjector(DependencyInjector[WebClients]):
    def __init__(self, session: aiohttp.ClientSession):
        self.session = session

    def build(self) -> WebClients:
        return WebClients(
            html_client=BaseAioHttpClient(session=self.session, resource_type=HtmlPage),
        )
