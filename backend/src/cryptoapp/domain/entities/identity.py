from dataclasses import dataclass

from cryptoapp.domain.exceptions import IdentityNotSetError


@dataclass(frozen=True)
class Identity:
    _value: int | None

    @property
    def value(self) -> int:
        if not self._value:
            raise IdentityNotSetError()
        return self._value
