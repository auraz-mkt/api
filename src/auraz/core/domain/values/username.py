from typing import Annotated, NewType

import regex
from annotated_types import Predicate

from auraz.core.domain.validation import Validation, ValidationResult, check_is_valid, validate_or_raise
from auraz.core.domain.values.localized_str import LStr

username_validations: list[Validation] = [
    Validation(
        pattern=regex.compile(r"[^a-zA-Z0-9._]"),
        should_match=False,
        error_message=LStr(
            en_US="Username must have only lowercase letters (a-z), uppercase letters (A-Z), numbers (0-9), underscores (_), or dots (.)",
            pt_BR="Nome de usuário deve ter apenas letras minúsculas (a-z), letras maiúsculas (A-Z), números (0-9), sublinhados (_), ou pontos (.)",
        ),
    ),
    Validation(
        pattern=regex.compile(r"^.{0,2}$"),
        should_match=False,
        error_message=LStr(
            en_US="Username must have at least three characters",
            pt_BR="Nome de usuário deve ter pelo menos três caracteres",
        ),
    ),
    Validation(
        pattern=regex.compile(r"^[\d.]"),
        should_match=False,
        error_message=LStr(
            en_US="Username cannot start with digit (0-9) or dot (.)",
            pt_BR="Nome de usuário não pode começar com dígitos (0-9) ou ponto (.)",
        ),
    ),
    Validation(
        pattern=regex.compile(r".*?[.]$"),
        should_match=False,
        error_message=LStr(
            en_US="Username cannot end with a dot (.)",
            pt_BR="Nome de usuário não deve começar com ponto (.)",
        ),
    ),
    Validation(
        pattern=regex.compile(r"[._][._]"),
        should_match=False,
        error_message=LStr(
            en_US="Username cannot have consecutive dot (.) and/or underscore (_)",
            pt_BR="Nome de usuário não pode ter pontos (.) e/ou sublinhados (_) consecutivos",
        ),
    ),
]


def validate_auraz_username_or_raise(candidate_username: str) -> ValidationResult:
    return validate_or_raise(candidate_username, username_validations)


def is_auraz_username(candidate_username: str) -> bool:
    return check_is_valid(candidate_username, username_validations)


AurazUsername = NewType("AurazUsername", Annotated[str, Predicate(is_auraz_username)])
