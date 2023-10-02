from auraz.core.domain.values.localized_str import LStr


class AurazException(Exception):
    cause: LStr

    def __init__(self, cause: LStr):
        self.cause = cause
        super().__init__()

    def __str__(self) -> str:
        return self.cause.en_US
