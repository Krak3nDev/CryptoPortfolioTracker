class DomainError(Exception):
    def __init__(self, message: str | None = None) -> None:
        super().__init__(message or "Domain Error")


class ValidationError(Exception):
    def __init__(self, message: str | None = None) -> None:
        super().__init__(message or "Validation Error")


class InvalidEmail(ValidationError):
    def __init__(self, email: str) -> None:
        message = f"Email validation error: {email}"
        super().__init__(message)


class UserAlreadyExistsError(DomainError):
    def __init__(self, username: str, email: str) -> None:
        self.username = username
        super().__init__(
            f"User with username: '{username}' or email: '{email} already exists"
        )


class UserAlreadyActivated(DomainError):
    def __init__(self, username: str) -> None:
        self.username = username
        super().__init__("User already activated")
