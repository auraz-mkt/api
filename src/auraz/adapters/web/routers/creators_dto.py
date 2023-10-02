from datetime import date

from pydantic.networks import AnyHttpUrl
from pydantic.types import PositiveFloat, PositiveInt

from auraz.adapters.web.routers.attributes_dto import AttributeResponse
from auraz.adapters.web.types.web_code import WebCode
from auraz.adapters.web.types.web_exchange import WebExchange
from auraz.adapters.web.types.web_username import WebUsername
from auraz.core.domain.entities.attribute import Gender, Category, Region
from auraz.core.domain.entities.creator import (
    CreatorPersonalInfo,
    EnrichedCreator,
    CreatorAttributes,
)
from auraz.core.domain.values.tiktok import (
    TikTokCreatorProfile,
    TikTokCreatorStatistics,
    TikTokUsername,
    TikTokVideo,
    TikTokVideoID,
)


class CreatorPersonalInfoResponse(WebExchange):
    full_name: str
    birth_date: date

    @classmethod
    def create_from(cls, domain: CreatorPersonalInfo):
        return CreatorPersonalInfoResponse(
            full_name=domain.full_name,
            birth_date=domain.birth_date,
        )


class CreatorAttributesResponse(WebExchange):
    categories: list[AttributeResponse[Category]]
    gender: AttributeResponse[Gender]
    region: AttributeResponse[Region]

    @classmethod
    def create_from(cls, domain: CreatorAttributes):
        # We need to use `model_construct` to bypass validation
        # to avoid Pydantic clashing with the generic types
        return CreatorAttributesResponse.model_construct(
            categories=list(map(lambda category: AttributeResponse[Category].create_from(category), domain.categories)),
            gender=AttributeResponse[Gender].create_from(domain.gender),
            region=AttributeResponse[Region].create_from(domain.region),
        )


class CreatorTikTokVideoResponse(WebExchange):
    id: TikTokVideoID
    title: str
    thumbnail: AnyHttpUrl

    @classmethod
    def create_from(cls, domain: TikTokVideo):
        return CreatorTikTokVideoResponse(
            id=domain.id,
            title=domain.title,
            thumbnail=AnyHttpUrl(str(domain.thumbnail)),
        )


class CreatorTikTokVideosResponse(WebExchange):
    data: list[CreatorTikTokVideoResponse]

    @classmethod
    def create_from(cls, domain: list[TikTokVideo]):
        return CreatorTikTokVideosResponse(
            data=list(map(lambda video: CreatorTikTokVideoResponse.create_from(video), domain))
        )


class CreatorTikTokStatisticsResponse(WebExchange):
    likes: PositiveInt
    followers: PositiveInt
    publications: PositiveInt

    @classmethod
    def create_from(cls, domain: TikTokCreatorStatistics):
        return CreatorTikTokStatisticsResponse(
            likes=domain.likes,
            followers=domain.followers,
            publications=domain.publications,
        )


class CreatorTikTokProfileResponse(WebExchange):
    username: TikTokUsername
    statistics: CreatorTikTokStatisticsResponse

    @classmethod
    def create_from(cls, domain: TikTokCreatorProfile):
        return CreatorTikTokProfileResponse(
            username=domain.username,
            statistics=CreatorTikTokStatisticsResponse.create_from(domain.statistics),
        )


class EnrichedCreatorResponse(WebExchange):
    webcode: WebCode
    username: WebUsername
    picture: AnyHttpUrl
    personal_info: CreatorPersonalInfoResponse
    attributes: CreatorAttributesResponse
    tiktok_profile: CreatorTikTokProfileResponse
    engagement: PositiveFloat

    @classmethod
    def create_from(cls, domain: EnrichedCreator):
        return EnrichedCreatorResponse(
            webcode=WebCode.from_id(domain.id),
            username=WebUsername.from_auraz_username(domain.username),
            picture=AnyHttpUrl(str(domain.picture)),
            personal_info=CreatorPersonalInfoResponse.create_from(domain.personal_info),
            attributes=CreatorAttributesResponse.create_from(domain.attributes),
            tiktok_profile=CreatorTikTokProfileResponse.create_from(domain.tiktok_profile),
            engagement=domain.engagement,
        )


class EnrichedCreatorsResponse(WebExchange):
    data: list[EnrichedCreatorResponse]

    @classmethod
    def create_from(cls, domain: list[EnrichedCreator]):
        return EnrichedCreatorsResponse(
            data=list(map(lambda creator: EnrichedCreatorResponse.create_from(creator), domain))
        )
