from typing import TypedDict

from sqlalchemy import select, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.asyncio import AsyncSession

from cryptoapp.infrastructure.persistence.gateways.base import (
    SessionInitializer,
)
from cryptoapp.infrastructure.persistence.tables import users_table


class UserCredentials(TypedDict):
    user_id: int
    email: str
    username: str
    is_active: bool



class UserReader(SessionInitializer):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def get_credentials(self, user_id: int) -> UserCredentials:
        stmt = (
            select(
                func.json_build_object(
                    "user_id",
                    users_table.c.user_id,
                    "email",
                    users_table.c.email,
                    "username",
                    users_table.c.username,
                    "is_active",
                    users_table.c.is_active,
                ).cast(JSONB)
            )
            .where(users_table.c.user_id == user_id)
        )
        return (await self._session.execute(stmt)).scalar_one()


