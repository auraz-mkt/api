from typing import Optional

from pydantic.networks import AnyHttpUrl
from pydantic.types import PositiveFloat

from auraz.adapters.web.types.localized_str import LocalizedStr
from auraz.adapters.web.types.web_code import WebCode
from auraz.adapters.web.types.web_exchange import WebExchange
from auraz.adapters.web.types.web_username import WebUsername
from auraz.core.domain.entities.attribute import Attribute
from auraz.core.domain.entities.creator import SearchedCreator
from auraz.core.domain.entities.filter import Filters


class SearchFilterResponse(WebExchange):
    webcode: WebCode
    label: LocalizedStr

    @classmethod
    def create_from(cls, attribute: Attribute):
        return SearchFilterResponse(
            webcode=WebCode.from_id(attribute.id),
            label=LocalizedStr.create_from(attribute.label),
        )


class SearchFiltersResponse(WebExchange):
    categories: list[SearchFilterResponse]
    genders: list[SearchFilterResponse]
    regions: list[SearchFilterResponse]

    @classmethod
    def create_from(cls, filters: Filters):
        def _convert_attributes_to_search_filters(attributes: list[Attribute]) -> list[SearchFilterResponse]:
            return list(map(lambda attribute: SearchFilterResponse.create_from(attribute), attributes))

        return SearchFiltersResponse(
            categories=_convert_attributes_to_search_filters(filters.categories),
            genders=_convert_attributes_to_search_filters(filters.genders),
            regions=_convert_attributes_to_search_filters(filters.regions),
        )


class SearchFiltersRequest(WebExchange):
    gender: Optional[WebCode]
    categories: list[WebCode]


class CreatorSearchRequest(WebExchange):
    filters: SearchFiltersRequest


class CreatorSearchResponse(WebExchange):
    username: WebUsername
    full_name: str
    picture: AnyHttpUrl
    engagement: PositiveFloat

    @classmethod
    def create_from(cls, creator: SearchedCreator):
        return CreatorSearchResponse(
            username=WebUsername.from_auraz_username(creator.username),
            full_name=creator.personal_info.full_name,
            picture=AnyHttpUrl(str(creator.picture)),
            engagement=creator.engagement,
        )


class CreatorsSearchResponse(WebExchange):
    data: list[CreatorSearchResponse]

    @classmethod
    def create_from(cls, creators: list[SearchedCreator]):
        return CreatorsSearchResponse(data=[CreatorSearchResponse.create_from(creator) for creator in creators])
