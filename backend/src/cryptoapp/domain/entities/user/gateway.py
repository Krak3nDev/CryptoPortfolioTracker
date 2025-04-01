from abc import abstractmethod
from typing import TypedDict

from websockets import Protocol

from cryptoapp.domain.entities.user.user import User, UserId


class UserAvailabilityInfo(TypedDict):
    username: str
    email: str


class UserGateway(Protocol):
    @abstractmethod
    async def by_identity(self, user_id: UserId) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def by_username(self, username: str) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def get_username_email_availability(
        self, username: str, email: str
    ) -> UserAvailabilityInfo | None:
        raise NotImplementedError

    @abstractmethod
    def add(self, user: User) -> None:
        raise NotImplementedError
