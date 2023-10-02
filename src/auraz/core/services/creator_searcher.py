from typing import Callable, Optional, cast

from auraz.core.domain.entities.attribute import Attribute, Category, Gender, Region
from auraz.core.domain.entities.creator import Creator, SearchedCreator
from auraz.core.domain.entities.filter import Filters
from auraz.core.domain.values.id import ID
from auraz.core.domain.values.username import AurazUsername
from auraz.core.services.creator_enricher import CreatorEnricher
from auraz.ports.database.repository import Repository
from auraz.ports.integrations.tiktok import TikTok


class CreatorSearcher:
    def __init__(
        self,
        creators: Repository[Creator],
        categories: Repository[Category],
        genders: Repository[Gender],
        regions: Repository[Region],
        tiktok: TikTok,
        creator_enricher: CreatorEnricher,
    ):
        self.creators = creators

        self.categories = categories
        self.genders = genders
        self.regions = regions

        self.tiktok = tiktok
        self.creator_enricher = creator_enricher

    async def search_creators(
        self,
        filtered_gender_id: Optional[ID],
        filtered_categories_ids: list[ID],
    ) -> list[SearchedCreator]:
        filtered_gender = await self.genders.find_by_id(filtered_gender_id) if filtered_gender_id is not None else None
        filtered_categories = await self.categories.find_all(filtered_categories_ids)

        retrieved_creators = await self.creators.all()

        usernames = self.__filter_creators(retrieved_creators, filtered_gender, filtered_categories)

        return await self.creator_enricher.get_creators_with_pictures(usernames)

    async def get_filters(self) -> Filters:
        return Filters(
            categories=cast(list[Attribute], await self.categories.all()),
            genders=cast(list[Attribute], await self.genders.all()),
            regions=cast(list[Attribute], await self.regions.all()),
        )

    def __filter_creators(
        self, creators: list[Creator], filtered_gender: Optional[Gender], filtered_categories: list[Category]
    ) -> list[AurazUsername]:
        choose_creator = self.__make_choose_creator(filtered_gender, filtered_categories)
        return [creator.username for creator in filter(choose_creator, creators)]

    def __make_choose_creator(
        self, filtered_gender: Optional[Gender], filtered_categories: list[Category]
    ) -> Callable[[Creator], bool]:
        def _choose_creator_bound(creator: Creator) -> bool:
            return self.__choose_creator(creator, filtered_gender, filtered_categories)

        return _choose_creator_bound

    def __choose_creator(
        self, creator: Creator, filtered_gender: Optional[Gender], filtered_categories: list[Category]
    ) -> bool:
        matches_gender = self.__matches_gender(filtered_gender, creator.attributes.gender)
        intersects_categories = self.__intersects_categories(filtered_categories, creator.attributes.categories)

        if not matches_gender:
            return False
        if not intersects_categories:
            return False
        return True

    @staticmethod
    def __matches_gender(filtered_gender: Optional[Gender], creator_gender: Gender) -> bool:
        return filtered_gender is None or creator_gender == filtered_gender

    @staticmethod
    def __intersects_categories(filtered_categories: list[Category], creator_categories: list[Category]) -> bool:
        return not filtered_categories or bool(set(filtered_categories).intersection(set(creator_categories)))
