from abc import abstractmethod
from typing import Protocol

from cryptoapp.infrastructure.dto.user import UserLoginDTO, UserDTO


class Authenticator(Protocol):
    @abstractmethod
    async def authenticate(self, login_user: UserLoginDTO) -> UserDTO: ...
