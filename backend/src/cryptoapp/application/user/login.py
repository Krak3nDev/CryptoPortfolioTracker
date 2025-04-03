from dataclasses import dataclass

from cryptoapp.application.exceptions import (
    EmailNotVerifiedError,
    UserIsNotRegistered,
)
from cryptoapp.domain.entities.user.gateway import UserGateway


@dataclass
class LoginRequest:
    username: str


class LoginInteractor:
    def __init__(self, user_gateway: UserGateway) -> None:
        self._user_gateway = user_gateway

    async def __call__(self, data: LoginRequest) -> None:
        user = await self._user_gateway.by_username(data.username)

        if not user:
            raise UserIsNotRegistered()

        if not user.is_active:
            raise EmailNotVerifiedError()
