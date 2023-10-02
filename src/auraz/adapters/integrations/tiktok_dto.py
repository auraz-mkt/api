from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from pydantic.networks import AnyHttpUrl
from pydantic.types import PositiveInt

from auraz.core.domain.values.count import Count
from auraz.core.domain.values.tiktok import TikTokCreatorAvatars, TikTokCreatorStatistics, TikTokVideo, TikTokVideoID
from auraz.core.domain.values.url import URL


class TikTokExchange(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class TikTokStatisticsRetrieval(TikTokExchange):
    followerCount: PositiveInt
    followingCount: PositiveInt
    friendCount: PositiveInt
    heartCount: PositiveInt
    videoCount: PositiveInt

    def to_domain(self) -> TikTokCreatorStatistics:
        return TikTokCreatorStatistics(
            likes=Count(self.heartCount),
            followers=Count(self.followerCount),
            publications=Count(self.videoCount),
        )


class TikTokAvatarsRetrieval(TikTokExchange):
    avatarThumb: AnyHttpUrl
    avatarMedium: AnyHttpUrl
    avatarLarger: AnyHttpUrl

    def to_domain(self) -> TikTokCreatorAvatars:
        return TikTokCreatorAvatars(
            small=URL(str(self.avatarThumb)),
            medium=URL(str(self.avatarMedium)),
            large=URL(str(self.avatarLarger)),
        )


class TikTokVideoMetadataRetrieval(TikTokExchange):
    cover: AnyHttpUrl


class TikTokVideoRetrieval(TikTokExchange):
    id: TikTokVideoID
    desc: str
    video: TikTokVideoMetadataRetrieval

    def to_domain(self) -> TikTokVideo:
        return TikTokVideo(id=self.id, title=self.desc, thumbnail=URL(str(self.video.cover)))
