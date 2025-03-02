from typing import NewType, cast

from fastapi import HTTPException
from redis.asyncio import Redis
from starlette import status
from starlette.requests import Request

from cryptoapp.application.common.id_provider import IdProvider
from cryptoapp.domain.entities.user.gateway import UserGateway
from cryptoapp.domain.entities.user.user import User

Activation_Token = NewType("Activation_Token", str)


def get_activation_token(request: Request) -> Activation_Token:
    token_str = request.path_params.get("token")
    if not token_str:
        raise HTTPException(status_code=400, detail="Missing 'token' path param")
    return Activation_Token(token_str)


# Business logic leaked to the adapter, but this was done deliberately, because I wanted it that way
class ActivationTokenIdProvider(IdProvider):
    def __init__(
        self, redis: Redis, token: Activation_Token, user_gateway: UserGateway
    ):
        self.redis = redis
        self.token = token
        self.user_gateway = user_gateway

    async def get_current_user_id(self) -> int:
        user_id = await self.redis.get(self.token)

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found for this activation token",
            )

        return int(user_id)

    async def get_user(self) -> User:
        user_id = await self.get_current_user_id()
        return cast(User, await self.user_gateway.by_identity(user_id))
