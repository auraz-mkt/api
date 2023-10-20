from typing import Any, Optional

from pydantic import model_serializer, model_validator

from auraz.adapters.web.types.web_exchange import WebExchange, get_value_from_exchange_or_raise
from auraz.core.domain.values.id import ID
from auraz.ports.security import id_concealer
from auraz.ports.security.access_token import Subject
from auraz.ports.security.id_concealer import Code


class WebCode(WebExchange):
    value: Code

    def __str__(self):
        return str(self.value)

    def to_id(self) -> ID:
        return id_concealer.get().decode(self.value)

    def to_subject(self) -> Subject:
        return Subject(self.value)

    @classmethod
    def from_id(cls, identifier: ID):
        return WebCode.model_construct(value=id_concealer.get().encode(identifier))

    @classmethod
    def from_subject(cls, subject: Subject):
        return WebCode.model_construct(value=Code(str(subject)))

    @model_serializer()
    def write(self) -> str:
        return str(self.value)

    # noinspection PyNestedDecorators
    @model_validator(mode="before")
    @classmethod
    def read(cls, data: Any) -> dict[str, str]:
        return get_value_from_exchange_or_raise(data=data, validated_type=WebCode)


def convert_webcode_to_id(webcode: Optional[WebCode]) -> Optional[ID]:
    return None if webcode is None else webcode.to_id()


def convert_webcodes_to_ids(webcodes: list[WebCode]) -> list[ID]:
    return [webcode.to_id() for webcode in webcodes]
