from auraz.adapters.web.authenticator import Authenticator
from auraz.adapters.web.routers.attributes_router import AttributesRouter
from auraz.adapters.web.routers.auth_router import AuthRouter
from auraz.adapters.web.routers.contacts_router import ContactsRouter
from auraz.adapters.web.routers.creators_router import CreatorsRouter
from auraz.adapters.web.routers.search_router import SearchRouter
from auraz.core.domain.entities.attribute import AttributeName, Category, Gender, Region
from auraz.ports.dependency_injection.dependency_injector import DependencyInjector
from auraz.ports.dependency_injection.types.database import Repositories
from auraz.ports.dependency_injection.types.integrations import Integrations
from auraz.ports.dependency_injection.types.security import Security
from auraz.ports.dependency_injection.types.services import Services
from auraz.ports.dependency_injection.types.web import WebRouters


class WebRouterDependencyInjector(DependencyInjector[WebRouters]):
    def __init__(
        self,
        security: Security,
        repositories: Repositories,
        integrations: Integrations,
        services: Services,
    ):
        self.security = security
        self.repositories = repositories
        self.integrations = integrations
        self.services = services

    def build(self) -> WebRouters:
        authenticator = Authenticator(self.repositories.users, self.security.access_token)

        return WebRouters(
            routers=[
                AuthRouter(
                    authenticator,
                    self.services.credentials_manager,
                ),
                AttributesRouter[Category](
                    name=AttributeName(singular="category", plural="categories"),
                    attributes=self.repositories.categories,
                ),
                AttributesRouter[Gender](
                    name=AttributeName(singular="gender", plural="genders"),
                    attributes=self.repositories.genders,
                ),
                AttributesRouter[Region](
                    name=AttributeName(singular="region", plural="regions"),
                    attributes=self.repositories.regions,
                ),
                ContactsRouter(
                    self.repositories.contacts,
                ),
                CreatorsRouter(
                    self.repositories.creators,
                    self.integrations.tiktok,
                    self.services.creator_enricher,
                ),
                SearchRouter(
                    self.services.creator_searcher,
                ),
            ]
        )
