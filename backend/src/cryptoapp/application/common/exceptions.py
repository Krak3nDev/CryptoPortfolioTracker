class ApplicationError(Exception):
    pass


class UserAlreadyExistsError(ApplicationError):
    def __init__(self, username: str) -> None:
        self.username = username
        super().__init__(f"User '{username}' already exists")


class InvalidTokenType(ApplicationError):
    pass


