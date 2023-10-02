from dataclasses import dataclass
from typing import Optional, cast

from regex import Pattern

from auraz.core.domain.exception import AurazException
from auraz.core.domain.values.localized_str import LStr


@dataclass
class Validation:
    pattern: Pattern
    should_match: bool
    error_message: LStr


class ValidationResult:
    def __init__(self, failed_validation: Optional[Validation]):
        self.failed_validation = failed_validation

    @property
    def is_valid(self) -> bool:
        return self.failed_validation is None


class DomainValidationException(AurazException):
    def __init__(self, candidate: str, failed_validation: Validation):
        super().__init__(
            cause=LStr(
                en_US=f"Candidate `{candidate}` does not attend validation. {failed_validation.error_message.en_US}",
                pt_BR=f"Candidato `{candidate}` não atende a validacão. {failed_validation.error_message.pt_BR}",
            )
        )


def _validate(candidate: str, validations: list[Validation]) -> ValidationResult:
    for validation in validations:
        has_matched = bool(validation.pattern.match(candidate))
        if has_matched != validation.should_match:
            return ValidationResult(failed_validation=validation)
    return ValidationResult(failed_validation=None)


def validate_or_raise(candidate: str, validations: list[Validation]):
    result = _validate(candidate, validations)

    if not result.is_valid:
        raise DomainValidationException(candidate, cast(Validation, result.failed_validation))


def check_is_valid(candidate: str, validations: list[Validation]) -> bool:
    return _validate(candidate, validations).is_valid
