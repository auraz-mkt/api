import json
from datetime import date
from typing import Optional

import regex
from async_lru import alru_cache

from auraz.adapters.integrations.tiktok_dto import (
    TikTokAvatarsRetrieval,
    TikTokVideoRetrieval,
    TikTokStatisticsRetrieval,
)
from auraz.core.domain.exception import AurazException
from auraz.core.domain.values.count import Count
from auraz.core.domain.values.localized_str import LStr
from auraz.core.domain.values.tiktok import TikTokCreatorAvatars, TikTokCreatorStatistics, TikTokUsername, TikTokVideo
from auraz.core.domain.values.url import URL
from auraz.ports.integrations.tiktok import TikTok
from auraz.ports.web.client import HtmlPage, Client

RETRY_DELAY = 2  # Retry in seconds

TIKTOK_DOMAIN_URL = URL("https://www.tiktok.com/")

TIKTOK_HOMEPAGE_STATE_PATTERN = regex.compile(
    r'<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__" type="application/json">(.*?)</script>'
)

TIKTOK_HOMEPAGE_WAITING_PATTERN = regex.compile(r"Please wait...")


class TikTokPageParsingException(AurazException):
    def __init__(self, tiktok_page: URL):
        self.tiktok_page = tiktok_page
        super().__init__(
            cause=LStr(
                en_US=f"Impossible to parse TikTok page `{self.tiktok_page}`",
                pt_BR=f"Impossível de analisar página do TikTok `{self.tiktok_page}`",
            )
        )


class TikTokScrapper(TikTok):
    def __init__(self, html_client: Client[HtmlPage]):
        self.html_client = html_client

    async def get_creator_avatars(self, username: TikTokUsername) -> TikTokCreatorAvatars:
        data = await self.__retrieve_data_from_profile(username)
        return self.__extract_avatars(data)

    async def get_creator_statistics(self, username: TikTokUsername) -> TikTokCreatorStatistics:
        data = await self.__retrieve_data_from_profile(username)
        return self.__extract_statistics(data)

    async def get_creator_videos(self, username: TikTokUsername, max_videos: Count) -> list[TikTokVideo]:
        data = await self.__retrieve_data_from_profile(username)
        return self.__extract_last_videos(data, max_videos)

    async def __retrieve_data_from_profile(self, tiktok_username: TikTokUsername) -> dict:
        return await self.__retrieve_data_from_profile_or_get_cached_data(
            username=tiktok_username,
            _ttl_hash=date.today(),
        )

    @alru_cache(maxsize=64)
    async def __retrieve_data_from_profile_or_get_cached_data(self, username: TikTokUsername, _ttl_hash: date) -> dict:
        profile_url = TIKTOK_DOMAIN_URL.with_path(f"/@{username}")

        profile = await self.html_client.retrieve_with_retry(
            url=profile_url,
            should_retry=self.__is_tiktok_page_loading,
        )

        data = self.__extract_tiktok_data_from_page(profile)

        if not data:
            raise TikTokPageParsingException(tiktok_page=profile_url)

        return data

    @staticmethod
    def __extract_avatars(data: dict) -> TikTokCreatorAvatars:
        user_data = data["__DEFAULT_SCOPE__"]["webapp.user-detail"]["userInfo"]["user"]
        return TikTokAvatarsRetrieval(**user_data).to_domain()

    @staticmethod
    def __extract_statistics(data: dict) -> TikTokCreatorStatistics:
        stats_data = data["__DEFAULT_SCOPE__"]["webapp.user-detail"]["userInfo"]["stats"]
        return TikTokStatisticsRetrieval(**stats_data).to_domain()

    @staticmethod
    def __extract_last_videos(data: dict, max_videos: int) -> list[TikTokVideo]:
        video_ids = data["__DEFAULT_SCOPE__"]["webapp.user-detail"]["userInfo"]["posts"]
        return [TikTokScrapper.__extract_video(data, video_id) for video_id in video_ids[:max_videos]]

    @staticmethod
    def __extract_video(data: dict, video_id: str) -> TikTokVideo:
        video = TikTokVideoRetrieval(**data["ItemModule"][video_id])
        return video.to_domain()

    @staticmethod
    def __extract_tiktok_data_from_page(page: HtmlPage) -> Optional[dict]:
        match = regex.search(pattern=TIKTOK_HOMEPAGE_STATE_PATTERN, string=str(page))
        return json.loads(match.group(1)) if match else None

    @staticmethod
    def __is_tiktok_page_loading(page: HtmlPage) -> bool:
        match = regex.search(pattern=TIKTOK_HOMEPAGE_WAITING_PATTERN, string=str(page))
        return bool(match)
