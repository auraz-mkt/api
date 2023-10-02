from typing import Type

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from auraz.core.domain.exception import AurazException
from auraz.core.domain.values.localized_str import LStr


def _beautify_wrong_value(value: str):
    if len(value) == 0:
        return LStr(en_US="Empty value", pt_BR="Valor vazio")
    return LStr(en_US=f"Value `{value}`", pt_BR=f"Valor `{value}`")


class WebExchangeValidationException(AurazException):
    def __init__(self, value: str, validated_type: Type):
        wrong_value = _beautify_wrong_value(value)
        type_name = validated_type.__name__

        super().__init__(
            cause=LStr(
                en_US=f"{wrong_value.en_US} is not valid for type `{type_name}`",
                pt_BR=f"{wrong_value.pt_BR} não é válido para o tipo `{type_name}`",
            )
        )


class WebExchange(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


def get_value_from_exchange_or_raise(data: str | dict[str, str], validated_type: Type):
    if isinstance(data, dict):
        return data
    if isinstance(data, str):
        return {"value": data}
    raise WebExchangeValidationException(value=data, validated_type=validated_type)
