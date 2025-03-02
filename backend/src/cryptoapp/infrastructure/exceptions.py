class UnauthorizedError(Exception):
    def __init__(self, message: str = "User is not authorized"):
        super().__init__(message)
