from dataclasses import dataclass


@dataclass(eq=True, frozen=True)
class LStr:
    pt_BR: str
    en_US: str
