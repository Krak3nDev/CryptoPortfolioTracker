from typing import Protocol

from cryptoapp.domain.entities.user.user import User


class IdProvider(Protocol):
    async def get_current_user_id(self) -> int: ...

    async def get_user(self) -> User: ...
