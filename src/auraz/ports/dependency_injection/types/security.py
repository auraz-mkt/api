from dataclasses import dataclass

from auraz.ports.dependency_injection.types.injectable import Injectable
from auraz.ports.security.id_concealer import IdConcealer


@dataclass(eq=True, frozen=True)
class Security(Injectable):
    id_concealer: IdConcealer
