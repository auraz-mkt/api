from abc import ABC, abstractmethod

from auraz.core.domain.values.count import Count
from auraz.core.domain.values.tiktok import TikTokCreatorAvatars, TikTokCreatorStatistics, TikTokUsername, TikTokVideo


class TikTok(ABC):
    @abstractmethod
    async def get_creator_avatars(self, username: TikTokUsername) -> TikTokCreatorAvatars:
        pass

    @abstractmethod
    async def get_creator_statistics(self, username: TikTokUsername) -> TikTokCreatorStatistics:
        pass

    @abstractmethod
    async def get_creator_videos(self, username: TikTokUsername, max_videos: Count) -> list[TikTokVideo]:
        pass
