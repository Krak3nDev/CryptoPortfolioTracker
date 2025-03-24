from dataclasses import dataclass

from cryptoapp.domain.entities.identity import Identity
from cryptoapp.domain.exceptions import UserAlreadyActivated


class UserId(Identity):
    pass


@dataclass
class User:
    _identity: UserId
    _email: str
    _hashed_password: str
    _username: str
    _is_active: bool

    @property
    def identity(self) -> int:
        return self._identity.value

    @property
    def email(self) -> str:
        return self._email

    @property
    def username(self) -> str:
        return self._username

    @property
    def hashed_password(self) -> str:
        return self._hashed_password

    @property
    def is_active(self) -> bool:
        return self._is_active

    def activate(self) -> None:
        if self._is_active:
            raise UserAlreadyActivated()
        self._is_active = True
