from contextlib import asynccontextmanager

import aiohttp
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from auraz.adapters.dependency_injectors.database_in_memory import DatabaseInMemoryDependencyInjector
from auraz.adapters.dependency_injectors.integrations import IntegrationsDependencyInjector
from auraz.adapters.dependency_injectors.security import SecurityDependencyInjector
from auraz.adapters.dependency_injectors.web_clients import WebClientsDependencyInjector
from auraz.adapters.dependency_injectors.web_exception_handlers import WebExceptionHandlerDependencyInjector
from auraz.adapters.dependency_injectors.web_routers import WebRouterDependencyInjector
from auraz.adapters.settings import Settings
from auraz.core.dependency_injectors.services import ServicesDependencyInjector
from auraz.ports.dependency_injection.types.web import WebExceptionHandlers, WebRouters

# Since all API endpoints are prefixed with a version (e.g., `/v1`),
# the default endpoint is available for the documentation
API_DOCS_PATH = "/"


def _inject_routers(api: FastAPI, web_routers: WebRouters):
    for router in web_routers.routers:
        api.include_router(router.create())


def _inject_exception_handlers(api: FastAPI, web_exception_handlers: WebExceptionHandlers):
    for handler in web_exception_handlers.exception_handlers:
        api.add_exception_handler(handler.exception_type, handler.handle_exception)


@asynccontextmanager
async def _setup(api: FastAPI, settings: Settings):
    async with aiohttp.ClientSession() as session:
        clients = WebClientsDependencyInjector(session).build()
        security = SecurityDependencyInjector(settings).build()
        repositories = DatabaseInMemoryDependencyInjector(settings).build()
        integrations = IntegrationsDependencyInjector(clients).build()
        services = ServicesDependencyInjector(security, repositories, integrations).build()
        routers = WebRouterDependencyInjector(security, repositories, integrations, services).build()

        _inject_routers(api, routers)
        yield


def _create_api(settings: Settings):
    new_api = FastAPI(
        title="Auraz API",
        version="0.1.0",
        summary="Auraz - Bringing Marketing Back to People",
        contact={
            "name": "Auraz Dev Team",
            "email": "auraz.mkt+dev@gmail.com",
            "url": "https://auraz.com.br/about",
        },
        docs_url=API_DOCS_PATH,
        redoc_url=None,  # Prefer Swagger to Redoc
        lifespan=lambda api: _setup(api, settings),
    )

    new_api.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_origins=settings.api.decoded_allowed_origins,
        allow_methods=settings.api.allowed_methods,
        allow_headers=settings.api.allowed_headers,
    )

    exception_handlers = WebExceptionHandlerDependencyInjector().build()
    _inject_exception_handlers(new_api, exception_handlers)

    return new_api


def _start_uvicorn(settings: Settings):
    uvicorn.run(
        app="auraz.api:auraz_api",
        host=str(settings.api.host),
        port=settings.api.port,
        reload=settings.api.should_reload,
    )


auraz_settings = Settings.load()
auraz_api = _create_api(auraz_settings)

if __name__ == "__main__":
    # Launch API with `poetry run python -m auraz.api`
    _start_uvicorn(auraz_settings)
