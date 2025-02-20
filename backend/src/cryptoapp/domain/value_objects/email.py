import re
from dataclasses import dataclass

from cryptoapp.domain.exceptions import InvalidEmail


@dataclass(slots=True, frozen=True, eq=True)
class Email:
    _value: str

    def __post_init__(self) -> None:
        pattern = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

        if not re.match(pattern, self._value):
            raise InvalidEmail(self._value)

    @property
    def value(self) -> str:
        return self._value
