import re
from dataclasses import dataclass

from cryptoapp.domain.exceptions import InvalidEmail, InvalidFieldLength

PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


EMAIL_LENGTH = 320


@dataclass(slots=True, frozen=True, eq=True)
class Email:
    value: str

    def __post_init__(self) -> None:
        if not re.match(PATTERN, self.value):
            raise InvalidEmail(self.value)

        if len(self.value) > EMAIL_LENGTH:
            raise InvalidFieldLength(
                field_name="email", value=self.value, max_length=EMAIL_LENGTH
            )
