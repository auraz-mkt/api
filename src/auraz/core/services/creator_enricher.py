import asyncio
from decimal import Decimal

from auraz.core.domain.entities.creator import Creator, EnrichedCreator, SearchedCreator
from auraz.core.domain.values.count import Count
from auraz.core.domain.values.percentage import Percentage
from auraz.core.domain.values.tiktok import TikTokVideo
from auraz.core.domain.values.username import AurazUsername
from auraz.ports.database.repository import Repository
from auraz.ports.integrations.tiktok import TikTok

MAX_VIDEOS = Count(6)

DEFAULT_ENGAGEMENT = Percentage(Decimal(42.69))  # TODO: Discuss default engagement algorithm


class CreatorEnricher:
    def __init__(
        self,
        creators: Repository[Creator],
        tiktok: TikTok,
    ):
        self.creators = creators
        self.tiktok = tiktok

    async def get_creator_last_videos(self, username: AurazUsername) -> list[TikTokVideo]:
        creator = await self.creators.find_by_key(key="username", value=username)
        return await self.tiktok.get_creator_videos(creator.tiktok_username, max_videos=MAX_VIDEOS)

    async def get_creators_last_videos(self, usernames: list[AurazUsername]) -> list[list[TikTokVideo]]:
        tasks = [asyncio.ensure_future(self.get_creator_last_videos(username)) for username in usernames]
        return list(await asyncio.gather(*tasks))

    async def get_creator_with_social_data(self, username: AurazUsername) -> EnrichedCreator:
        creator = await self.creators.find_by_key(key="username", value=username)
        avatars = await self.tiktok.get_creator_avatars(creator.tiktok_username)
        statistics = await self.tiktok.get_creator_statistics(creator.tiktok_username)

        return EnrichedCreator.create_from(
            creator, engagement=DEFAULT_ENGAGEMENT, avatars=avatars, statistics=statistics
        )

    async def get_creators_with_social_data(self, usernames: list[AurazUsername]) -> list[EnrichedCreator]:
        tasks = [asyncio.ensure_future(self.get_creator_with_social_data(username)) for username in usernames]
        return list(await asyncio.gather(*tasks))

    async def get_creator_with_pictures(self, username: AurazUsername) -> SearchedCreator:
        creator = await self.creators.find_by_key(key="username", value=username)
        avatars = await self.tiktok.get_creator_avatars(creator.tiktok_username)

        return SearchedCreator.create_from(creator, engagement=DEFAULT_ENGAGEMENT, picture=avatars.small)

    async def get_creators_with_pictures(self, usernames: list[AurazUsername]) -> list[SearchedCreator]:
        tasks = [asyncio.ensure_future(self.get_creator_with_pictures(username)) for username in usernames]
        return list(await asyncio.gather(*tasks))
