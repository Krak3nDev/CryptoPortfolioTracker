from abc import abstractmethod

from websockets import Protocol

from cryptoapp.domain.entities.user.user import User


class UserGateway(Protocol):
    @abstractmethod
    async def by_identity(self, user_id: int) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def is_username_or_email_taken(self, username: str, email: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def add(self, user: User) -> None:
        raise NotImplementedError
