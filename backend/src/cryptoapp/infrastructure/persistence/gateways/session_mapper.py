from redis.asyncio import Redis
from typing_extensions import TypedDict


class Session(TypedDict):
    user_id: int

SESSION_TTL = 7200

class SessionGateway:
    def __init__(self, redis: Redis) -> None:
        self._redis = redis

    async def create_session(self, session_id: str, user_id: str) -> None:
        await self._redis.setex(name=session_id, value=user_id, time=SESSION_TTL)

    async def delete_session(self, session_id: str) -> None:
        await self._redis.delete(session_id)

    async def refresh_session(self, session_id: str) -> None:
        await self._redis.expire(session_id, SESSION_TTL)

    async def by_id(self, session_id: str) -> Session | None:
        user_id = await self._redis.get(session_id)

        if not user_id:
            return None

        session: Session = {
            "user_id": int(user_id),
        }
        return session
