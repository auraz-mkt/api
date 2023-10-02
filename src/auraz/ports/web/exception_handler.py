from abc import ABC, abstractmethod
from typing import Any, Callable, Coroutine, Generic, Type, TypeVar

from fastapi import Request
from fastapi.responses import JSONResponse

from auraz.core.domain.exception import AurazException

E = TypeVar("E", bound=AurazException)


Handler = Callable[[Request, E], Coroutine[Any, Any, JSONResponse]]


class ExceptionHandler(ABC, Generic[E]):
    def __init__(self, exception_type: Type[E]):
        self.exception_type = exception_type

    @abstractmethod
    def handle_exception(self, request: Request, exception: E):
        pass
