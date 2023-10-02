from pydantic import Field

from auraz.adapters.web.types.web_exchange import WebExchange
from auraz.core.domain.values.localized_str import LStr


class LocalizedStr(WebExchange):
    pt_BR: str = Field(serialization_alias="pt-BR")
    en_US: str = Field(serialization_alias="en-US")

    @classmethod
    def create_from(cls, domain: LStr):
        return LocalizedStr(
            pt_BR=domain.pt_BR,
            en_US=domain.en_US,
        )
