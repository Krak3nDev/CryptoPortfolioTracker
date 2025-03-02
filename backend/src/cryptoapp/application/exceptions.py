class ApplicationError(Exception):
    pass


class EmailNotVerifiedError(ApplicationError):
    def __init__(self, message: str = "User email is not verified"):
        super().__init__(message)


class UserIsNotRegistered(ApplicationError):
    def __init__(self, message: str = "User is not registered"):
        super().__init__(message)
