from dataclasses import dataclass
from typing import Optional

from .user_id import UserId
from ..exceptions import UserNotActiveError, AlreadyActivatedException


@dataclass
class User:
    id: UserId
    username: str
    email: Optional[str]
    password: Optional[str]
    is_active: bool

    def ensure_is_active(self) -> None:
        if not self.is_active:
            raise UserNotActiveError()

    def ensure_not_already_active(self) -> None:
        if self.is_active:
            raise AlreadyActivatedException()
