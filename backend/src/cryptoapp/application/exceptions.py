from cryptoapp.domain.exceptions import BaseNotFound


class ApplicationError(Exception):
    pass


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


class EmailNotVerifiedError(ApplicationError):
    def __init__(self, message: str = "User email is not verified") -> None:
        super().__init__(message)


class UserIsNotRegistered(BaseNotFound):
    def __init__(self, message: str = "User is not registered") -> None:
        super().__init__(message)
