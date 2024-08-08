from abc import abstractmethod
from typing import Optional, Protocol

from cryptoapp.application.dto.user import (
    CreateUserDTO,
)
from cryptoapp.domain.entities.user import User


class UserRepo(Protocol):
    @abstractmethod
    async def create_user(self, user: CreateUserDTO) -> User:
        pass

    @abstractmethod
    async def change_active_status(self, user_id: int, is_active: bool) -> None:
        pass

    @abstractmethod
    async def check_user_data_unique(self, username: str, email: str) -> bool:
        pass

    @abstractmethod
    async def get_user_by_username(self, username: str) -> Optional[User]:
        pass

    @abstractmethod
    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        pass
