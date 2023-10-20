from passlib.context import CryptContext
from passlib.handlers.argon2 import argon2

from auraz.core.domain.values.password import AurazEncryptedPassword, AurazRawPassword
from auraz.ports.security.password_manager import CorruptedPasswordException, PasswordManager


class PasslibPasswordManager(PasswordManager):
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

    def verify(self, raw_password: AurazRawPassword, encrypted_password: AurazEncryptedPassword) -> bool:
        if not argon2.identify(encrypted_password):
            raise CorruptedPasswordException(encrypted_password)

        return self.pwd_context.verify(secret=str(raw_password), hash=str(encrypted_password))

    def encrypt(self, raw_password: AurazRawPassword) -> AurazEncryptedPassword:
        return AurazEncryptedPassword(self.pwd_context.hash(str(raw_password)))
