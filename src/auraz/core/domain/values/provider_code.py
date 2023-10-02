from typing import Annotated, NewType

import regex
from annotated_types import Predicate

from auraz.core.domain.validation import (
    Validation,
    ValidationResult,
    check_is_valid,
    validate_or_raise,
)
from auraz.core.domain.values.localized_str import LStr

provider_code_validations: list[Validation] = [
    Validation(
        pattern=regex.compile(r"[\p{Cc}\p{Cn}\p{Cs}\p{Cf}]"),
        should_match=False,
        error_message=LStr(
            en_US="Third party code must have only printable characters",
            pt_BR="Código de terceiros deve ter apenas caracteres imprimíveis",
        ),
    ),
]


def validate_provider_code_or_raise(candidate_provider_code: str) -> ValidationResult:
    return validate_or_raise(candidate_provider_code, provider_code_validations)


def is_provider_code(candidate_provider_code: str) -> bool:
    return check_is_valid(candidate_provider_code, provider_code_validations)


ProviderCode = NewType("ProviderCode", Annotated[str, Predicate(is_provider_code)])
