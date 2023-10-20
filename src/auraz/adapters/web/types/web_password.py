from typing import Any

from pydantic import model_serializer, model_validator

from auraz.adapters.web.types.web_exchange import WebExchange, get_value_from_exchange_or_raise
from auraz.core.domain.values.password import AurazRawPassword, validate_auraz_raw_password_or_raise


class WebPassword(WebExchange):
    value: str

    def to_auraz_raw_password(self) -> AurazRawPassword:
        return AurazRawPassword(self.value)

    @classmethod
    def from_auraz_raw_password(cls, password: AurazRawPassword):
        return WebPassword.model_construct(value=str(password))

    @model_serializer()
    def write(self) -> str:
        return self.value

    # noinspection PyNestedDecorators
    @model_validator(mode="before")
    @classmethod
    def read(cls, data: Any) -> dict[str, str]:
        identifier = get_value_from_exchange_or_raise(data=data, validated_type=WebPassword)
        validate_auraz_raw_password_or_raise(candidate_raw_password=identifier["value"])
        return identifier
