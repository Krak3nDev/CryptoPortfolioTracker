class DomainError(Exception):
    def __init__(self, message: str | None = None) -> None:
        super().__init__(message or "Domain Error")


class UserAlreadyExistsError(DomainError):
    def __init__(
        self, username: str | None = None, email: str | None = None
    ) -> None:
        self.username = username
        self.email = email

        details: list[str] = []
        if username:
            details.append(f"username='{username}'")
        if email:
            details.append(f"email='{email}'")

        fields_str = ", ".join(details)
        super().__init__(f"User with {fields_str} already exists")


class BaseNotFound(Exception):
    def __init__(self, message: str = "Resource not found") -> None:
        super().__init__(message)


class EntityNotFound(BaseNotFound):
    def __init__(self, field_name: str, value: int) -> None:
        message = f"{field_name} with ID {value} not found"
        super().__init__(message)
