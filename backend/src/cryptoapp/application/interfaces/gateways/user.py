from abc import abstractmethod
from typing import Optional, Protocol

from cryptoapp.domain.entities.user import User
from cryptoapp.infrastructure.dto.user import CreateUserDTO, UserDTO


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
    async def get_with_password(self, username: str) -> Optional[UserDTO]:
        pass
