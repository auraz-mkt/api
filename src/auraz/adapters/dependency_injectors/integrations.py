from auraz.adapters.integrations.tiktok_scrapper import TikTokScrapper
from auraz.ports.dependency_injection.dependency_injector import DependencyInjector
from auraz.ports.dependency_injection.types.integrations import Integrations
from auraz.ports.dependency_injection.types.web import WebClients


class IntegrationsDependencyInjector(DependencyInjector[Integrations]):
    def __init__(self, web_clients: WebClients):
        self.web_clients = web_clients

    def build(self) -> Integrations:
        return Integrations(
            tiktok=TikTokScrapper(html_client=self.web_clients.html_client),
        )
