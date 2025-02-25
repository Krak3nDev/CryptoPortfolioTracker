from dataclasses import dataclass

from cryptoapp.domain.exceptions import InvalidFieldLength

USERNAME_LENGTH = 50


@dataclass(slots=True, frozen=True, eq=True)
class Username:
    value: str

    def __post_init__(self) -> None:
        if len(self.value) > USERNAME_LENGTH:
            raise InvalidFieldLength(
                field_name="username", value=self.value, max_length=USERNAME_LENGTH
            )
