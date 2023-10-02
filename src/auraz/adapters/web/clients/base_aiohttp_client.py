import asyncio
from http import HTTPStatus
from typing import Callable, Type, cast

from aiohttp import ClientSession

from auraz.core.domain.values.url import URL
from auraz.ports.web.client import Client, Resource, ResourceNotRetrievableException

AIOHTTP_CLIENT_RETRY_DELAY = 2  # Retry in seconds


class BaseAioHttpClient(Client[Resource]):
    def __init__(self, session: ClientSession, resource_type: Type[Resource]):
        self.session = session
        self.resource_type = resource_type

    async def retrieve_with_retry(self, url: URL, should_retry: Callable[[Resource], bool]) -> Resource:
        page = await self.retrieve(url)

        if should_retry(page):
            await asyncio.sleep(delay=AIOHTTP_CLIENT_RETRY_DELAY)
            page = await self.retrieve(url)

        return page

    async def retrieve(self, url: URL) -> Resource:
        async with self.session.get(url) as response:
            if response.status == HTTPStatus.OK:
                return cast(Resource, await response.text())

            raise ResourceNotRetrievableException(
                url=url,
                status=HTTPStatus(response.status),
                resource_type=self.resource_type,
            )
