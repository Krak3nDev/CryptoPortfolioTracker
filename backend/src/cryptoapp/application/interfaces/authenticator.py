from abc import abstractmethod
from typing import Protocol

from cryptoapp.application.dto.user import UserAccessDTO, UserLoginDTO
from cryptoapp.domain.entities.user import User


class Authenticator(Protocol):
    @abstractmethod
    async def authenticate(self, login_user: UserLoginDTO) -> User: ...
