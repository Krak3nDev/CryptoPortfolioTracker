from cryptoapp.domain.exceptions import BaseNotFound


class ApplicationError(Exception):
    pass


class EmailNotVerifiedError(ApplicationError):
    def __init__(self, message: str = "User email is not verified") -> None:
        super().__init__(message)


class UserIsNotRegistered(BaseNotFound):
    def __init__(self, message: str = "User is not registered") -> None:
        super().__init__(message)
