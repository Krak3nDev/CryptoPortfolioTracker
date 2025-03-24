from cryptoapp.domain.exceptions import NotFound


class ApplicationError(Exception):
    pass


class EmailNotVerifiedError(ApplicationError):
    def __init__(self, message: str = "User email is not verified") -> None:
        super().__init__(message)


class UserIsNotRegistered(NotFound):
    def __init__(self, message: str = "User is not registered") -> None:
        super().__init__(message)
