from dataclasses import dataclass

from auraz.core.services.creator_enricher import CreatorEnricher
from auraz.core.services.creator_searcher import CreatorSearcher


@dataclass(eq=True, frozen=True)
class Services:
    creator_enricher: CreatorEnricher
    creator_searcher: CreatorSearcher
