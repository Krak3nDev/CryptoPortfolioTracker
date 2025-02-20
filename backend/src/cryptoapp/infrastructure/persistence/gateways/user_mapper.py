from sqlalchemy import exists, or_, select

from cryptoapp.domain.entities.user.gateway import UserGateway
from cryptoapp.domain.entities.user.user import User
from cryptoapp.infrastructure.persistence.gateways.base import SessionInitializer
from cryptoapp.infrastructure.persistence.tables.users import users_table


class UserMapper(SessionInitializer, UserGateway):
    async def by_identity(self, user_id: int) -> User | None:
        return await self._session.get(User, user_id)

    def add(self, user: User) -> None:
        self._session.add(user)

    async def is_username_or_email_taken(self, username: str, email: str) -> bool:
        query = select(
            exists().where(
                or_(users_table.c.username == username, users_table.c.email == email)
            )
        )
        return (await self._session.execute(query)).scalar_one()
