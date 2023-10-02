import logging
from http import HTTPStatus
from typing import Generic, Type

from starlette.requests import Request
from starlette.responses import JSONResponse

from auraz.core.domain.values.localized_str import LStr
from auraz.ports.web.exception_handler import E, ExceptionHandler


class BaseExceptionHandler(ExceptionHandler[E], Generic[E]):
    def __init__(self, exception_type: Type[E], status_code: HTTPStatus, conceal_cause: bool = False):
        self.status_code = status_code
        self.conceal_cause = conceal_cause
        super().__init__(exception_type)

    async def handle_exception(self, _request: Request, exception: E):
        logging.exception(exception)

        cause = self.__extract_cause(exception)

        return JSONResponse(
            status_code=self.status_code.value,
            content={
                "error": {
                    "description": self.status_code.description,
                    "cause": {
                        "en-US": cause.en_US,
                        "pt-BR": cause.pt_BR,
                    },
                }
            },
        )

    def __extract_cause(self, exception: E) -> LStr:
        if self.conceal_cause:
            return LStr(en_US="[REDACTED]", pt_BR="[SUPRIMIDO]")
        return exception.cause
