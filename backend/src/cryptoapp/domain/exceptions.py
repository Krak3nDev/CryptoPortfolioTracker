class DomainError(Exception):
    def __init__(self, message: str | None = None) -> None:
        super().__init__(message or "Domain Error")


class IdentityNotSetError(DomainError):
    def __init__(self, message: str = "The identity has not been set.") -> None:
        super().__init__(message)


class ValidationError(Exception):
    def __init__(self, message: str | None = None) -> None:
        super().__init__(message or "Validation Error")


class InvalidEmail(ValidationError):
    def __init__(self, email: str) -> None:
        message = f"Email validation error: {email}"
        super().__init__(message)


class InvalidFieldLength(ValidationError):
    def __init__(self, field_name: str, value: str, max_length: int) -> None:
        message = (
            f"The field '{field_name}' is too long: '{value}'. "
            f"The maximum allowed length is {max_length} characters."
        )
        super().__init__(message)


class UserAlreadyExistsError(DomainError):
    def __init__(self, username: str | None = None, email: str | None = None) -> None:
        details: list[str] = []
        if username:
            details.append(f"username='{username}'")
        if email:
            details.append(f"email='{email}'")

        fields_str = ", ".join(details)
        super().__init__(f"User with {fields_str} already exists")


class UserAlreadyActivated(DomainError):
    def __init__(self) -> None:
        super().__init__("User already activated")


class BaseNotFound(Exception):
    def __init__(self, message: str = "Resource not found") -> None:
        super().__init__(message)


class EntityNotFound(BaseNotFound):
    def __init__(self, field_name: str, value: int) -> None:
        message = f"{field_name} with ID {value} not found"
        super().__init__(message)
