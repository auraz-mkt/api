from dataclasses import dataclass

from auraz.ports.security.id_concealer import IdConcealer


@dataclass(eq=True, frozen=True)
class Security:
    id_concealer: IdConcealer
