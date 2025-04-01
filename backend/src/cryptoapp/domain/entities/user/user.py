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

    @classmethod
    def create(
        cls,
        user_id: int | None,
        email: str,
        hashed_password: str,
        username: str,
    ) -> "User":
        return cls(
            _identity=UserId(user_id),
            _email=email,
            _hashed_password=hashed_password,
            _username=username,
            _is_active=False,
        )

    @property
    def identity(self) -> UserId:
        return self._identity

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
