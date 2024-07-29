from cryptoapp.application.common.exceptions import ApplicationError


class DomainError(Exception):
    pass


class UserNotActiveError(DomainError):
    pass


class AlreadyActivatedException(DomainError):
    pass
