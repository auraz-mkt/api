from abc import ABC, abstractmethod

from auraz.core.domain.exception import AurazException
from auraz.core.domain.values.localized_str import LStr
from auraz.core.domain.values.password import AurazEncryptedPassword, AurazRawPassword


class CorruptedPasswordException(AurazException):
    def __init__(self, encrypted_password: AurazEncryptedPassword):
        super().__init__(
            cause=LStr(
                en_US=f"Password cannot be parsed by the selected encryption algorithm: `{encrypted_password}`",
                pt_BR=f"Senha não pode ser analisada pelo algoritmo criptográfico selecionado: `{encrypted_password}`",
            )
        )


class PasswordManager(ABC):
    @abstractmethod
    def verify(self, raw_password: AurazRawPassword, encrypted_password: AurazEncryptedPassword) -> bool:
        pass

    @abstractmethod
    def encrypt(self, raw_password: AurazRawPassword) -> AurazEncryptedPassword:
        pass
