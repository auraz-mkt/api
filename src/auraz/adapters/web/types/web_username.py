from typing import Any

from pydantic import model_serializer, model_validator

from auraz.adapters.web.types.web_exchange import WebExchange, get_value_from_exchange_or_raise
from auraz.core.domain.values.username import AurazUsername, validate_auraz_username_or_raise


class WebUsername(WebExchange):
    value: str

    def to_auraz_username(self) -> AurazUsername:
        return AurazUsername(self.value)

    @classmethod
    def from_auraz_username(cls, username: AurazUsername):
        return WebUsername(value=str(username))

    @model_serializer()
    def write(self) -> str:
        return self.value

    # noinspection PyNestedDecorators
    @model_validator(mode="before")
    @classmethod
    def read(cls, data: Any) -> dict[str, str]:
        identifier = get_value_from_exchange_or_raise(data=data, validated_type=WebUsername)
        validate_auraz_username_or_raise(candidate_username=identifier["value"])
        return identifier
