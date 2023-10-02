from fastapi import APIRouter

from auraz.adapters.web.routers.search_dto import CreatorSearchRequest, CreatorsSearchResponse
from auraz.adapters.web.routers.search_dto import SearchFiltersResponse
from auraz.adapters.web.types.web_code import convert_webcode_to_id, convert_webcodes_to_ids
from auraz.core.services.creator_searcher import CreatorSearcher
from auraz.ports.web.router import Router


class SearchRouter(Router):
    def __init__(self, creator_searcher: CreatorSearcher):
        self.creator_searcher = creator_searcher

    def create(self) -> APIRouter:
        router = APIRouter(tags=["Search"])

        @router.get("/v1/filters")
        async def list_filters() -> SearchFiltersResponse:
            filters = await self.creator_searcher.get_filters()
            return SearchFiltersResponse.create_from(filters)

        @router.post("/v1/search_creators")
        async def search_creators(request: CreatorSearchRequest) -> CreatorsSearchResponse:
            found_creators = await self.creator_searcher.search_creators(
                convert_webcode_to_id(request.filters.gender),
                convert_webcodes_to_ids(request.filters.categories),
            )

            return CreatorsSearchResponse.create_from(found_creators)

        return router
