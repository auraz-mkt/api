from dataclasses import dataclass

from auraz.core.services.creator_enricher import CreatorEnricher
from auraz.core.services.creator_searcher import CreatorSearcher
from auraz.ports.dependency_injection.types.injectable import Injectable


@dataclass(eq=True, frozen=True)
class Services(Injectable):
    creator_enricher: CreatorEnricher
    creator_searcher: CreatorSearcher
