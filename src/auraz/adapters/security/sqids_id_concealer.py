from sqids import Sqids  # type: ignore

from auraz.core.domain.values.id import ID
from auraz.ports.security.id_concealer import Code, CodeLength, IdConcealer

CODE_MIN_LENGTH = CodeLength(8)


class SquidsIdConcealer(IdConcealer):
    def __init__(self, alphabet):
        self.sqids = Sqids(min_length=CODE_MIN_LENGTH, alphabet=alphabet)

    @property
    def min_code_length(self) -> CodeLength:
        return CODE_MIN_LENGTH

    def decode(self, code: Code) -> ID:
        return ID(self.sqids.decode(str(code))[0])

    def encode(self, identifier: ID) -> Code:
        return Code(self.sqids.encode([identifier]))
