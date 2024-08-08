from abc import abstractmethod
from typing import Optional, Protocol

from cryptoapp.application.dto.user import (
    CreateUserDTO, UserAuthDTO,
)
from cryptoapp.domain.entities.user import User


class UserGateway(Protocol):
    @abstractmethod
    async def add(self, user: CreateUserDTO) -> User:
        pass

    @abstractmethod
    async def change_active_status(self, user_id: int, is_active: bool) -> None:
        pass

    @abstractmethod
    async def check_data_unique(self, username: str, email: str) -> bool:
        pass

    @abstractmethod
    async def get_by_username(self, username: str) -> Optional[User]:
        pass

    @abstractmethod
    async def get_by_id(self, user_id: int) -> Optional[User]:
        pass

    @abstractmethod
    async def get_current_user_with_password(self, username: str) -> Optional[UserAuthDTO]:
        pass
