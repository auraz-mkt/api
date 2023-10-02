from dataclasses import dataclass

from auraz.ports.dependency_injection.types.injectable import Injectable
from auraz.ports.integrations.tiktok import TikTok


@dataclass(eq=True, frozen=True)
class Integrations(Injectable):
    tiktok: TikTok
