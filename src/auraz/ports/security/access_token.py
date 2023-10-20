from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import NewType


JWT = NewType("JWT", str)
Subject = NewType("Subject", str)
MaxAge = NewType("MaxAge", timedelta)
Expiration = NewType("Expiration", datetime)


class AccessToken(ABC):
    @abstractmethod
    def encode(self, subject: Subject, max_age: MaxAge) -> tuple[JWT, Expiration]:
        pass

    @abstractmethod
    def decode(self, token: JWT) -> tuple[Subject, MaxAge, Expiration]:
        pass
