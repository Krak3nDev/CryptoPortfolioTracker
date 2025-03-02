import uuid
from dataclasses import dataclass

from starlette.requests import Request
from starlette.responses import Response

from cryptoapp.infrastructure.persistence.gateways.session_mapper import SessionGateway


@dataclass
class SessionCookieDTO:
    key: str
    value: str
    httponly: bool


class HTTPSessionManager:
    def __init__(self, session_mapper: SessionGateway):
        self._session_mapper = session_mapper

    async def init_session(self, user_id: int) -> SessionCookieDTO:
        session_id = str(uuid.uuid4())

        await self._session_mapper.create_session(
            session_id=session_id, user_id=str(user_id)
        )

        return SessionCookieDTO(key="session_id", value=session_id, httponly=True)

    async def invalidate_session(self, session_id: str) -> None:
        await self._session_mapper.delete_session(session_id)


class FastAPISessionManager:
    def __init__(self, http_session_manager: HTTPSessionManager) -> None:
        self._http_session_manager = http_session_manager

    async def init_session(self, user_id: int, response: Response) -> None:
        session_cookie = await self._http_session_manager.init_session(user_id)
        response.set_cookie(
            key=session_cookie.key,
            value=session_cookie.value,
            httponly=session_cookie.httponly,
            secure=False,
            samesite="lax",
        )

    async def invalidate_session(self, request: Request, response: Response) -> None:
        session_id = request.cookies.get("session_id")

        await self._http_session_manager.invalidate_session(session_id)

        response.delete_cookie(key="session_id")
