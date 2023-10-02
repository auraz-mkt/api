from typing import Generic

from auraz.adapters.web.types.localized_str import LocalizedStr
from auraz.adapters.web.types.web_code import WebCode
from auraz.adapters.web.types.web_exchange import WebExchange
from auraz.core.domain.entities.attribute import AttributeType


class AttributeResponse(WebExchange, Generic[AttributeType]):
    webcode: WebCode
    label: LocalizedStr

    @classmethod
    def create_from(cls, attribute: AttributeType):
        return AttributeResponse[AttributeType](
            webcode=WebCode.from_id(attribute.id),
            label=LocalizedStr.create_from(attribute.label),
        )


class AttributesResponse(WebExchange, Generic[AttributeType]):
    data: list[AttributeResponse[AttributeType]]

    @classmethod
    def create_from(cls, attributes: list[AttributeType]):
        return AttributesResponse[AttributeType](
            data=list(map(lambda attribute: AttributeResponse.create_from(attribute), attributes))
        )
