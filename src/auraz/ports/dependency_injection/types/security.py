from dataclasses import dataclass

from auraz.ports.dependency_injection.types.injectable import Injectable
from auraz.ports.security.id_concealer import IdConcealer
from auraz.ports.security.access_token import AccessToken
from auraz.ports.security.password_manager import PasswordManager


@dataclass(eq=True, frozen=True)
class Security(Injectable):
    id_concealer: IdConcealer
    access_token: AccessToken
    password_manager: PasswordManager
