from typing import cast

from sqlalchemy import or_, select

from cryptoapp.domain.entities.user.gateway import UserAvailabilityInfo, UserGateway
from cryptoapp.domain.entities.user.user import User
from cryptoapp.infrastructure.persistence.gateways.base import SessionInitializer
from cryptoapp.infrastructure.persistence.tables.users import users_table


class UserMapper(SessionInitializer, UserGateway):
    async def by_identity(self, user_id: int) -> User | None:
        result = await self._session.get(User, user_id)
        return cast(User | None, result)

    async def by_username(self, username: str) -> User | None:
        stmt = select(User).where(users_table.c.username == username)
        result = (await self._session.execute(stmt)).scalar_one_or_none()
        return cast(User | None, result)

    def add(self, user: User) -> None:
        self._session.add(user)

    async def get_username_email_availability(
        self, username: str, email: str
    ) -> UserAvailabilityInfo | None:
        query = select(users_table.c.username, users_table.c.email).where(
            or_(users_table.c.username == username, users_table.c.email == email)
        )

        result = await self._session.execute(query)
        row = result.fetchone()

        if row is not None:
            return {"username": row[0], "email": row[1]}

        return None
