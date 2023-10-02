from auraz.core.services.creator_enricher import CreatorEnricher
from auraz.core.services.creator_searcher import CreatorSearcher
from auraz.ports.dependency_injection.types.database import Repositories
from auraz.ports.dependency_injection.types.integrations import Integrations
from auraz.ports.dependency_injection.types.services import Services


class ServicesDependencyInjector:
    def __init__(self, repositories: Repositories, integrations: Integrations):
        self.repositories = repositories
        self.integrations = integrations

    def build(self) -> Services:
        creator_enricher = CreatorEnricher(
            self.repositories.creators,
            self.integrations.tiktok,
        )
        creator_searcher = CreatorSearcher(
            self.repositories.creators,
            self.repositories.categories,
            self.repositories.genders,
            self.repositories.regions,
            self.integrations.tiktok,
            creator_enricher,
        )

        return Services(
            creator_enricher=creator_enricher,
            creator_searcher=creator_searcher,
        )
