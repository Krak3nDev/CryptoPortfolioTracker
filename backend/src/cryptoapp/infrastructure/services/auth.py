from dataclasses import dataclass

from fastapi import HTTPException

from cryptoapp.application.exceptions import UserIsNotRegistered
from cryptoapp.domain.entities.user.hasher import PasswordHasher
from cryptoapp.infrastructure.persistence.gateways.user_mapper import UserMapper


@dataclass
class LoginAuthDTO:
    username: str
    password: str


class Auther:
    def __init__(self, hasher: PasswordHasher, user_mapper: UserMapper):
        self._hasher = hasher
        self._user_mapper = user_mapper

    async def authenticate(self, data: LoginAuthDTO) -> int:
        user = await self._user_mapper.by_username(username=data.username)

        if not user:
            raise UserIsNotRegistered()

        is_valid_password = self._hasher.verify(
            password=data.password, hashed_password=user.get_hashed_password()
        )

        if (data.username != user.get_username()) or not is_valid_password:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        return user.identity
