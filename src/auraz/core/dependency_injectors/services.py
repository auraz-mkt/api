from auraz.core.services.creator_enricher import CreatorEnricher
from auraz.core.services.creator_searcher import CreatorSearcher
from auraz.core.services.credentials_manager import CredentialsManager
from auraz.ports.dependency_injection.types.database import Repositories
from auraz.ports.dependency_injection.types.integrations import Integrations
from auraz.ports.dependency_injection.types.security import Security
from auraz.ports.dependency_injection.types.services import Services


class ServicesDependencyInjector:
    def __init__(
        self,
        security: Security,
        repositories: Repositories,
        integrations: Integrations,
    ):
        self.security = security
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
        credentials_manager = CredentialsManager(
            self.repositories.users,
            self.security.password_manager,
        )

        return Services(
            creator_enricher=creator_enricher,
            creator_searcher=creator_searcher,
            credentials_manager=credentials_manager,
        )
