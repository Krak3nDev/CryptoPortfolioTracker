class InfrastructureError(Exception):
    pass


class AuthenticationError(InfrastructureError):
    pass


class InvalidTokenType(InfrastructureError):
    pass
