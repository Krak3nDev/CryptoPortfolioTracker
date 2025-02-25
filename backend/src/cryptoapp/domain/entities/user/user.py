from dataclasses import dataclass

from cryptoapp.domain.entities.user.user_id import UserId
from cryptoapp.domain.exceptions import UserAlreadyActivated
from cryptoapp.domain.value_objects.email import Email
from cryptoapp.domain.value_objects.username import Username


@dataclass
class User:
    _identity: UserId
    _email: Email
    _hashed_password: str
    _username: Username
    _is_active: bool

    @property
    def identity(self) -> int:
        return self._identity.value

    @property
    def get_email(self) -> str:
        return self._email.value

    @property
    def get_username(self) -> str:
        return self._username.value

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
