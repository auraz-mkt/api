from abc import ABC, abstractmethod
from http import HTTPStatus
from typing import Callable, Generic, NewType, Type, TypeVar

from auraz.core.domain.exception import AurazException
from auraz.core.domain.values.localized_str import LStr
from auraz.core.domain.values.url import URL

HtmlPage = NewType("HtmlPage", str)

Resource = TypeVar("Resource", bound=HtmlPage)


class ResourceNotRetrievableException(AurazException):
    def __init__(self, url: URL, status: HTTPStatus, resource_type: Type[Resource]):
        self.url = url
        self.status = status
        self.resource_type = resource_type

        super().__init__(
            cause=LStr(
                en_US=f"Could not retrieve `{self.resource_type}` from URL `{self.url}` (status: {self.status}).",
                pt_BR=f"Não foi possível recuperar `{self.resource_type}` da URL `{self.url}` (status: {self.status}).",
            )
        )


class Client(ABC, Generic[Resource]):
    @abstractmethod
    async def retrieve_with_retry(self, url: URL, should_retry: Callable[[Resource], bool]) -> Resource:
        pass

    @abstractmethod
    async def retrieve(self, url: URL) -> Resource:
        pass
