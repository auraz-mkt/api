from dataclasses import dataclass

from auraz.core.domain.entities.entity import Entity
from auraz.core.domain.values.email import AurazEmail
from auraz.core.domain.values.password import AurazRawPassword


@dataclass(frozen=True)
class User(Entity):
    email: AurazEmail
    raw_password: AurazRawPassword
