from dataclasses import dataclass
from datetime import date

from auraz.core.domain.entities.attribute import Category, Gender, Region
from auraz.core.domain.entities.entity import Entity
from auraz.core.domain.entities.user import User
from auraz.core.domain.values.percentage import Percentage
from auraz.core.domain.values.tiktok import (
    TikTokCreatorAvatars,
    TikTokCreatorProfile,
    TikTokCreatorStatistics,
    TikTokUsername,
)
from auraz.core.domain.values.url import URL
from auraz.core.domain.values.username import AurazUsername


@dataclass(frozen=True)
class CreatorPersonalInfo(Entity):
    full_name: str
    birth_date: date


@dataclass(frozen=True)
class CreatorAttributes(Entity):
    categories: list[Category]
    gender: Gender
    region: Region


@dataclass(frozen=True)
class Creator(Entity):
    user: User
    username: AurazUsername
    personal_info: CreatorPersonalInfo
    attributes: CreatorAttributes
    tiktok_username: TikTokUsername

    @property
    def email(self):
        return self.user.email

    @classmethod
    def create_from(
        cls,
        user: User,
        username: AurazUsername,
        personal_info: CreatorPersonalInfo,
        attributes: CreatorAttributes,
        tiktok_username: TikTokUsername,
    ):
        return Creator(
            id=user.id,
            user=user,
            username=username,
            personal_info=personal_info,
            attributes=attributes,
            tiktok_username=tiktok_username,
        )


@dataclass(frozen=True)
class SearchedCreator(Entity):
    user: User
    username: AurazUsername
    personal_info: CreatorPersonalInfo
    engagement: Percentage
    picture: URL

    @property
    def email(self):
        return self.user.email

    @classmethod
    def create_from(cls, creator: Creator, engagement: Percentage, picture: URL):
        return SearchedCreator(
            id=creator.id,
            user=creator.user,
            username=creator.username,
            personal_info=creator.personal_info,
            engagement=engagement,
            picture=picture,
        )


@dataclass(frozen=True)
class EnrichedCreator(Entity):
    user: User
    username: AurazUsername
    personal_info: CreatorPersonalInfo
    attributes: CreatorAttributes
    tiktok_profile: TikTokCreatorProfile
    engagement: Percentage
    picture: URL

    @property
    def email(self):
        return self.user.email

    @classmethod
    def create_from(
        cls,
        creator: Creator,
        engagement: Percentage,
        avatars: TikTokCreatorAvatars,
        statistics: TikTokCreatorStatistics,
    ):
        return EnrichedCreator(
            id=creator.id,
            user=creator.user,
            username=creator.username,
            personal_info=creator.personal_info,
            attributes=creator.attributes,
            tiktok_profile=TikTokCreatorProfile(
                username=creator.tiktok_username,
                avatars=avatars,
                statistics=statistics,
            ),
            engagement=engagement,
            picture=avatars.small,
        )
