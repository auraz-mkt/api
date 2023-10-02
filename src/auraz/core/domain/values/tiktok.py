from dataclasses import dataclass
from typing import Annotated, NewType

import regex
from annotated_types import Predicate

from auraz.core.domain.values.count import Count
from auraz.core.domain.values.url import URL

TIKTOK_USERNAME_PATTERN = regex.compile(
    r"""
    (?![\d.])          # Lookahead: No start digit or dot
    (?!.*?[.]$)        # Lookahead: No end dot 
    (?!.*?([._][._]))  # Lookahead: No double dot or underscore
    [\w.]+             # Match valid characters
    """,
    regex.VERBOSE,
)


def is_tiktok_username(candidate_username: str) -> bool:
    return bool(TIKTOK_USERNAME_PATTERN.fullmatch(candidate_username))


TikTokVideoID = NewType("TikTokVideoID", str)
TikTokUsername = NewType("TikTokUsername", Annotated[str, Predicate(is_tiktok_username)])


@dataclass(frozen=True)
class TikTokVideo:
    id: TikTokVideoID
    title: str
    thumbnail: URL


@dataclass(frozen=True)
class TikTokCreatorAvatars:
    small: URL
    medium: URL
    large: URL


@dataclass(frozen=True)
class TikTokCreatorStatistics:
    likes: Count
    followers: Count
    publications: Count


@dataclass(frozen=True)
class TikTokCreatorProfile:
    username: TikTokUsername
    avatars: TikTokCreatorAvatars
    statistics: TikTokCreatorStatistics
