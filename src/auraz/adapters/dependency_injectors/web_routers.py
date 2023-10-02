from auraz.adapters.web.routers.attributes_router import AttributesRouter
from auraz.adapters.web.routers.creators_router import CreatorsRouter
from auraz.adapters.web.routers.search_router import SearchRouter
from auraz.core.domain.entities.attribute import AttributeName, Category, Gender, Region
from auraz.ports.dependency_injection.dependency_injector import DependencyInjector
from auraz.ports.dependency_injection.types.database import Repositories
from auraz.ports.dependency_injection.types.integrations import Integrations
from auraz.ports.dependency_injection.types.services import Services
from auraz.ports.dependency_injection.types.web import WebRouters


class WebRouterDependencyInjector(DependencyInjector[WebRouters]):
    def __init__(
        self,
        repositories: Repositories,
        integrations: Integrations,
        services: Services,
    ):
        self.repositories = repositories
        self.integrations = integrations
        self.services = services

    def build(self) -> WebRouters:
        return WebRouters(
            routers=[
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
