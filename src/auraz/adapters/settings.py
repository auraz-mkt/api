import os
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from textwrap import wrap
from typing import Annotated

import regex
from annotated_types import Predicate
from pydantic import AliasChoices, Field
from pydantic.networks import AnyHttpUrl, IPvAnyAddress
from pydantic.types import PositiveInt
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import Literal

from auraz.core.domain.values.url import URL

BASE64_PATTERN = regex.compile(
    r"""
    (?:-{5}BEGIN\s(?:PUBLIC|EC\sPRIVATE)\sKEY-{5})?    # Header
    (?:[A-Za-z0-9+/]{4})+                              # Multiple length 4 blocks
    (?:[A-Za-z0-9+/]{2}==)?                            # Optional end with `==`
    (?:-{5}END\s(?:PUBLIC|EC\sPRIVATE)\sKEY-{5})?      # Footer
    """,
    regex.VERBOSE,
)


def is_base64(value: str) -> bool:
    return bool(regex.fullmatch(BASE64_PATTERN, value))


Base64 = Annotated[str, Predicate(is_base64)]


class Mode(Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"


class AurazSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class APISettings(AurazSettings):
    model_config = SettingsConfigDict(env_prefix="api_")

    host: AnyHttpUrl | IPvAnyAddress
    # `port` accepts both `API_PORT` (API standard) or `PORT` (Heroku standard)
    # See: https://devcenter.heroku.com/articles/container-registry-and-runtime#dockerfile-commands-and-runtime
    port: PositiveInt = Field(validation_alias=AliasChoices("api_port", "port"))
    allowed_origins: list[AnyHttpUrl | Literal["*"]]
    allowed_methods: list[str]
    allowed_headers: list[str]
    mode: Mode

    @property
    def decoded_allowed_origins(self) -> list[str]:
        # We need to strip a trailing `/` from the end of the URL
        # because Pydantic's AnyHttpUrl adds it incorrectly,
        # causing a mismatch in the CORSMiddleware.
        #
        # Read more at:
        # - https://github.com/pydantic/pydantic/issues/7186
        return list(map(lambda url: str(url).rstrip("/"), self.allowed_origins))

    @property
    def should_reload(self) -> bool:
        match self.mode:
            case Mode.DEVELOPMENT:
                return True
            case Mode.PRODUCTION:
                return False


class SecuritySettings(AurazSettings):
    model_config = SettingsConfigDict(env_prefix="sec_")

    webcode_alphabet: str
    public_key: Base64
    private_key: Base64

    @property
    def parsed_public_key(self):
        key = [
            "-----BEGIN PUBLIC KEY-----",
            *wrap(self.public_key, width=64),
            "-----END PUBLIC KEY-----",
        ]
        return "\n".join(key)

    @property
    def parsed_private_key(self):
        key = [
            "-----BEGIN PRIVATE KEY-----",
            *wrap(self.private_key, width=64),
            "-----END PRIVATE KEY-----",
        ]
        return "\n".join(key)


class DatabaseSettings(AurazSettings):
    model_config = SettingsConfigDict(env_prefix="db_")

    connection: Path

    @property
    def url(self) -> URL:
        if isinstance(self.connection, Path):
            return URL(os.path.abspath(str(self.connection)))

        raise ValueError(f"Database connection is invalid {self.connection}")


@dataclass
class Settings:
    api: APISettings
    sec: SecuritySettings
    db: DatabaseSettings

    @classmethod
    def load(cls):
        return Settings(
            api=APISettings(),
            sec=SecuritySettings(),
            db=DatabaseSettings(),
        )
