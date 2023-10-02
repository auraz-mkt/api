from dataclasses import dataclass

from auraz.ports.integrations.tiktok import TikTok


@dataclass(eq=True, frozen=True)
class Integrations:
    tiktok: TikTok
