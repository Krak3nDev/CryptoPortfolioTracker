from dataclasses import dataclass


@dataclass
class UserId:
    _value: int | None

    @property
    def value(self) -> int:
        return self._value  # type: ignore

    @property
    def is_new(self) -> bool:
        return self._value is None
