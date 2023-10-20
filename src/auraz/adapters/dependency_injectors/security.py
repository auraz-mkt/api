from auraz.adapters.security.jose_access_token import JoseAccessToken
from auraz.adapters.security.passlib_password_manager import PasslibPasswordManager
from auraz.adapters.security.sqids_id_concealer import SquidsIdConcealer
from auraz.adapters.settings import Settings
from auraz.ports.dependency_injection.dependency_injector import DependencyInjector
from auraz.ports.dependency_injection.types.security import Security
from auraz.ports.security import id_concealer


class SecurityDependencyInjector(DependencyInjector[Security]):
    def __init__(self, settings: Settings):
        self.settings = settings

    def build(self) -> Security:
        id_concealer.initialize(SquidsIdConcealer(self.settings.sec.webcode_alphabet))

        return Security(
            id_concealer=id_concealer.get(),
            access_token=JoseAccessToken(
                public_key=self.settings.sec.parsed_public_key,
                private_key=self.settings.sec.parsed_private_key,
            ),
            password_manager=PasslibPasswordManager(),
        )
