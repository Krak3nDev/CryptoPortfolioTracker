import re
from typing import Final

from cryptoapp.domain.exceptions import InvalidFieldLength, InvalidEmail

PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

EMAIL_LENGTH: Final[int] = 320


def validate_length(max_length: int, field_name: str, value: str) -> None:
    if len(value) > max_length:
        raise InvalidFieldLength(
            field_name=field_name,
            value=value,
            max_length=max_length,
        )


def validate_email(value: str) -> None:
    if not re.match(PATTERN, value):
        raise InvalidEmail(value)

    if len(value) > EMAIL_LENGTH:
        raise InvalidFieldLength(
            field_name="email", value=value, max_length=EMAIL_LENGTH
        )
