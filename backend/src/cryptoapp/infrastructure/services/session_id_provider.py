from abc import abstractmethod
from typing import Protocol

from starlette.requests import Request

from cryptoapp.application.common.id_provider import IdProvider
from cryptoapp.application.exceptions import UserIsNotRegistered
from cryptoapp.domain.entities.user.gateway import UserGateway
from cryptoapp.domain.entities.user.user import User
from cryptoapp.infrastructure.exceptions import UnauthorizedError
from cryptoapp.infrastructure.persistence.gateways.session_mapper import (
    Session,
    SessionGateway,
)


class SessionIDGetter(Protocol):
    @abstractmethod
    def get(self) -> str | None: ...


class FastAPISessionIDGetter(SessionIDGetter):
    def __init__(self, request: Request) -> None:
        self._request = request

    def get(self) -> str | None:
        return self._request.cookies.get("session_id")


class HTTPIdentityProvider(IdProvider):
    def __init__(
        self,
        session_id_getter: SessionIDGetter,
        session_mapper: SessionGateway,
        user_mapper: UserGateway,
    ):
        self._session_mapper = session_mapper
        self._user_mapper = user_mapper
        self._session_id_getter = session_id_getter
        self._active_session: Session | None = None

    async def _get_active_session(self) -> Session:
        if self._active_session:
            return self._active_session

        session_id = self._session_id_getter.get()
        if not session_id:
            raise UnauthorizedError()

        active_session = await self._session_mapper.by_id(session_id)

        if not active_session:
            raise UnauthorizedError()

        await self._session_mapper.refresh_session(session_id)

        self._active_session = active_session
        return active_session

    async def get_current_user_id(self) -> int:
        session = await self._get_active_session()
        return session["user_id"]

    async def get_user(self) -> User:
        user_id = await self.get_current_user_id()
        user = await self._user_mapper.by_identity(user_id)

        if not user:
            raise UserIsNotRegistered()

        return user
