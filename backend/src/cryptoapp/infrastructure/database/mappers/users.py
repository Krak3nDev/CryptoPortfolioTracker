from typing import Optional, Any

from sqlalchemy import Update, exists, or_, select, Row
from sqlalchemy.dialects.postgresql import Insert

from cryptoapp.application.interfaces.gateways.user import UserGateway
from cryptoapp.domain.entities.user import User
from cryptoapp.infrastructure.database.models import UserDB
from .base import SessionInitializer
from ...dto.data import CreateUserDTO, UserDTO


class UserDataMapper(UserGateway, SessionInitializer):
    def _load(self, row: Row[Any]) -> User:
        return User(
            id=row.user_id,
            username=row.username,
            is_active=row.is_active,
            email=row.email,
        )

    def _load_dto(self, row: Row[Any]) -> UserDTO:
        return UserDTO(
            id=row.user_id,
            username=row.username,
            password=row.password,
            email=row.email,
            is_active=row.is_active,
        )

    async def add(self, user: CreateUserDTO) -> User:
        statement = (
            Insert(UserDB)
            .values(
                full_name=user.full_name,
                username=user.username,
                email=user.email,
                password_hash=user.password,
            )
            .returning(UserDB.user_id, UserDB.username)
        )
        result = (await self.session.execute(statement)).one()
        return self._load(result)

    async def change_active_status(self, user_id: int, is_active: bool) -> None:
        stmt = (
            Update(UserDB).where(UserDB.user_id == user_id).values(is_active=is_active)
        )
        await self.session.execute(stmt)

    async def check_data_unique(self, username: str, email: str) -> bool:
        statement = select(
            exists().where(or_(UserDB.username == username, UserDB.email == email))
        )
        result = await self.session.execute(statement)
        return result.scalar_one()

    async def get_by_username(self, username: str) -> Optional[User]:
        statement = select(UserDB).where(UserDB.username == username)
        result = (await self.session.execute(statement)).one_or_none()
        if result:
            return self._load(result)
        return None

    async def get_by_id(self, user_id: int) -> Optional[User]:
        statement = select(UserDB).where(UserDB.user_id == user_id)
        result = (await self.session.execute(statement)).one_or_none()
        if result:
            return self._load(result)
        return None

    async def get_with_password(self, username: str) -> Optional[UserDTO]:
        statement = select(UserDB).where(UserDB.username == username)
        result = (await self.session.execute(statement)).one_or_none()
        if result:
            return self._load_dto(result)
        return None
