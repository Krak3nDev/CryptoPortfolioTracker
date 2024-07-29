from typing import Optional

from cryptoapp.application.dto.user import (
    BasicUserDTO,
    CreateUserDTO,
)
from cryptoapp.application.interfaces.repositories.user import UserRepo
from cryptoapp.domain.entities.user import User
from cryptoapp.infrastructure.database.models import UserDB
from sqlalchemy import Update, exists, or_, select
from sqlalchemy.dialects.postgresql import Insert

from .base import BaseRepo


class SQLAlchemyUserRepo(UserRepo, BaseRepo):
    async def create_user(self, user: CreateUserDTO) -> BasicUserDTO:
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
        return BasicUserDTO(
            result.user_id,
            result.username,
        )

    async def change_active_status(self, user_id: int, is_active: bool) -> None:
        stmt = (
            Update(UserDB).where(UserDB.user_id == user_id).values(is_active=is_active)
        )
        await self.session.execute(stmt)

    async def check_user_data_unique(self, username: str, email: str) -> bool:
        statement = select(
            exists().where(or_(UserDB.username == username, UserDB.email == email))
        )
        result = await self.session.execute(statement)
        return result.scalar_one()

    async def get_user_by_username(self, username: str) -> Optional[User]:
        statement = select(UserDB).where(UserDB.username == username)
        result = (await self.session.execute(statement)).scalar_one_or_none()
        return (
            User(
                id=result.user_id,
                username=result.username,
                password=result.password_hash,
                is_active=result.is_active,
                email=result.email,
            )
            if result
            else None
        )

    async def get_user_by_id(self, user_id: int) -> User:
        statement = select(UserDB).where(UserDB.user_id == user_id)
        result = (await self.session.execute(statement)).scalar_one()
        return User(
            id=result.user_id,
            username=result.username,
            password=result.password_hash,
            is_active=result.is_active,
            email=result.email,
        )
