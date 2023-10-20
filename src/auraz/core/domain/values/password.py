from typing import Annotated, NewType

import regex
from annotated_types import Predicate

from auraz.core.domain.validation import Validation, ValidationResult, check_is_valid, validate_or_raise
from auraz.core.domain.values.localized_str import LStr

raw_password_validations: list[Validation] = [
    Validation(
        pattern=regex.compile(r"[\p{Cc}\p{Cn}\p{Cs}\p{Cf}]"),
        should_match=False,
        error_message=LStr(
            en_US="Password must have only printable characters",
            pt_BR="Senha deve ter apenas caracteres imprimíveis",
        ),
    ),
    Validation(
        pattern=regex.compile(r"^.{0,7}$"),
        should_match=False,
        error_message=LStr(
            en_US="Password must have at least eight characters",
            pt_BR="Senha deve ter pelo menos oito caracteres",
        ),
    ),
]


def validate_auraz_raw_password_or_raise(candidate_raw_password: str) -> ValidationResult:
    return validate_or_raise(candidate_raw_password, raw_password_validations)


def is_auraz_raw_password(candidate_raw_password: str) -> bool:
    return check_is_valid(candidate_raw_password, raw_password_validations)


AurazRawPassword = NewType("AurazRawPassword", Annotated[str, Predicate(is_auraz_raw_password)])
AurazEncryptedPassword = NewType("AurazEncryptedPassword", str)
