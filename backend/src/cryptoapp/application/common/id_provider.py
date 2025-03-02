from abc import abstractmethod
from typing import Protocol

from cryptoapp.domain.entities.user.user import User


class IdProvider(Protocol):
    @abstractmethod
    async def get_current_user_id(self) -> int: ...

    @abstractmethod
    async def get_user(self) -> User: ...
