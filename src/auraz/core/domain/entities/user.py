from dataclasses import dataclass

from auraz.core.domain.entities.entity import Entity
from auraz.core.domain.values.email import AurazEmail
from auraz.core.domain.values.password import AurazRawPassword, AurazEncryptedPassword


@dataclass(frozen=True)
class Credentials:
    email: AurazEmail
    raw_password: AurazRawPassword


@dataclass(frozen=True)
class User(Entity):
    email: AurazEmail
    encrypted_password: AurazEncryptedPassword
