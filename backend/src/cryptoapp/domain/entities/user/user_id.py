class UserId:
    def __init__(self, value: int | None = None) -> None:
        self._value = value

    @property
    def value(self) -> int:
        return self._value  # type: ignore

    @property
    def is_new(self) -> bool:
        return self._value is None

    def __composite_values__(self) -> tuple[int | None]:
        return (self._value,)
