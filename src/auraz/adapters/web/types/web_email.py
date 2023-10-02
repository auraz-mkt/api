from typing import Any

from pydantic import model_serializer, model_validator

from auraz.adapters.web.types.web_exchange import WebExchange, get_value_from_exchange_or_raise
from auraz.core.domain.values.email import AurazEmail, validate_auraz_email_or_raise


class WebEmail(WebExchange):
    value: str

    def to_auraz_email(self) -> AurazEmail:
        return AurazEmail(self.value)

    @classmethod
    def from_auraz_email(cls, password: AurazEmail):
        return WebEmail.model_construct(value=str(password))

    @model_serializer()
    def write(self) -> str:
        return self.value

    # noinspection PyNestedDecorators
    @model_validator(mode="before")
    @classmethod
    def read(cls, data: Any) -> dict[str, str]:
        identifier = get_value_from_exchange_or_raise(data=data, validated_type=WebEmail)
        validate_auraz_email_or_raise(candidate_email=identifier["value"])
        return identifier
