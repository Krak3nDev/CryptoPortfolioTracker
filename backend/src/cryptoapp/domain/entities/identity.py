from dataclasses import dataclass

from cryptoapp.domain.exceptions import DomainError


@dataclass(frozen=True)
class Identity:
    _value: int | None

    @property
    def value(self) -> int:
        if not self._value:
            raise DomainError("The identity has not been set.")
        return self._value
