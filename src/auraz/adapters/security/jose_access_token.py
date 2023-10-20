from datetime import datetime
from typing import NewType

from jose import jwk, jwt
from jose.backends.base import Key
from jose.constants import ALGORITHMS

from auraz.adapters.settings import Base64
from auraz.ports.security.access_token import AccessToken, Expiration, JWT, MaxAge, Subject

TOKEN_ENCRYPTION = ALGORITHMS.ES256
TOKEN_ISSUER = "https://api.auraz.com.br"
TOKEN_AUDIENCE = "https://auraz.com.br"


PEM = NewType("PEM", Base64)


class JoseAccessToken(AccessToken):
    def __init__(self, public_key: PEM, private_key: PEM):
        self.public_key: Key = self.__parse_key(public_key)
        self.private_key: Key = self.__parse_key(private_key)

    def encode(self, subject: Subject, max_age: MaxAge) -> tuple[JWT, Expiration]:
        creation_time = datetime.utcnow()
        expiration_time = creation_time + max_age

        claims = {
            "sub": str(subject),
            "iss": TOKEN_ISSUER,
            "aud": TOKEN_AUDIENCE,
            "nbf": creation_time,
            "iat": creation_time,
            "exp": expiration_time,
        }

        raw_token = jwt.encode(
            claims=claims,
            key=self.private_key,
            algorithm=TOKEN_ENCRYPTION,
        )

        return JWT(raw_token), Expiration(expiration_time)

    def decode(self, token: JWT) -> tuple[Subject, MaxAge, Expiration]:
        raw_token = str(token)

        claims = jwt.decode(
            token=raw_token,
            key=self.public_key,
            issuer=TOKEN_ISSUER,
            audience=TOKEN_AUDIENCE,
            algorithms=TOKEN_ENCRYPTION,
        )

        subject = str(claims["sub"])
        creation_time = datetime.fromtimestamp(int(claims["iat"]))
        expiration_time = datetime.fromtimestamp(int(claims["exp"]))

        max_age = expiration_time - creation_time

        return Subject(subject), MaxAge(max_age), Expiration(expiration_time)

    @staticmethod
    def __parse_key(pem: PEM) -> Key:
        return jwk.construct(pem, algorithm=TOKEN_ENCRYPTION)
