from fastapi import APIRouter

from auraz.adapters.web.routers.creators_dto import CreatorTikTokVideosResponse, EnrichedCreatorResponse
from auraz.adapters.web.types.web_username import WebUsername
from auraz.core.domain.entities.creator import Creator
from auraz.core.services.creator_enricher import CreatorEnricher
from auraz.ports.database.repository import Repository
from auraz.ports.integrations.tiktok import TikTok
from auraz.ports.web.router import Router


class CreatorsRouter(Router):
    def __init__(
        self,
        creators: Repository[Creator],
        tiktok: TikTok,
        creator_enricher: CreatorEnricher,
    ):
        self.creators = creators
        self.tiktok = tiktok
        self.creator_enricher = creator_enricher

    def create(self) -> APIRouter:
        router = APIRouter(tags=["Creators"])

        @router.get("/v1/creators/{code}")
        async def show_creator(code: str) -> EnrichedCreatorResponse:
            username = WebUsername(value=code)
            creator = await self.creator_enricher.get_creator_with_social_data(username.to_auraz_username())
            return EnrichedCreatorResponse.create_from(creator)

        @router.get("/v1/creators/{code}/videos")
        async def list_all_creator_videos(code: str) -> CreatorTikTokVideosResponse:
            username = WebUsername(value=code)
            videos = await self.creator_enricher.get_creator_last_videos(username.to_auraz_username())
            return CreatorTikTokVideosResponse.create_from(videos)

        return router
