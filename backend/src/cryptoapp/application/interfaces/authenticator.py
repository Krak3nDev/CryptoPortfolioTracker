from abc import abstractmethod
from typing import Protocol

from cryptoapp.application.dto.user import UserLoginDTO, UserAuthDTO


class Authenticator(Protocol):
    @abstractmethod
    async def authenticate(self, login_user: UserLoginDTO) -> UserAuthDTO: ...
