from typing import Annotated, NewType

import regex
from annotated_types import Predicate

from auraz.core.domain.validation import Validation, ValidationResult, check_is_valid, validate_or_raise
from auraz.core.domain.values.localized_str import LStr

# Validates emails according to W3C HTML5 email pattern,
# which willfully violates RFC 5332. See more at:
# - https://stackoverflow.com/q/201323
# - https://stackoverflow.com/a/8829363
W3C_HTML5_EMAIL_PATTERN = regex.compile(
    r"""
    ^
    [a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+  # Local
    @
    [a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*  # Domain
    $
    """,
    regex.VERBOSE | regex.IGNORECASE,
)

email_validations: list[Validation] = [
    Validation(
        pattern=W3C_HTML5_EMAIL_PATTERN,
        should_match=True,
        error_message=LStr(
            en_US="Email does not comply with W3C HTML5 specification",
            pt_BR="E-mail não obedece a especificação da W3C HTML5",
        ),
    ),
]


def validate_auraz_email_or_raise(candidate_email: str) -> ValidationResult:
    return validate_or_raise(candidate_email, email_validations)


def is_auraz_email(candidate_email: str) -> bool:
    print("candidate_email: '", candidate_email, "'")
    return check_is_valid(candidate_email, email_validations)


AurazEmail = NewType("AurazEmail", Annotated[str, Predicate(is_auraz_email)])
