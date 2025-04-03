import pytest
from cryptoapp.domain.entities.user.gateway import (
    UserAvailabilityInfo,
    UserGateway,
)
from cryptoapp.domain.entities.user.user import User, UserId


@pytest.fixture(scope="function")
def user():
    return User.create(
        user_id=1,
        email="test@example.com",
        hashed_password="hashed_password",
        username="testuser"
    )


@pytest.fixture(scope="function")
def user_gateway():
    class InMemoryUserGateway(UserGateway):
        def __init__(self):
            self._users = {}

        async def by_identity(self, user_id: UserId) -> User | None:
            return self._users.get(user_id)

        async def by_username(self, username: str) -> User | None:
            for user in self._users.values():
                if user.username == username:
                    return user
            return None

        async def get_username_email_availability(
            self, username: str, email: str
        ) -> UserAvailabilityInfo | None:
            for u in self._users.values():
                if u.username == username or u.email == email:
                    return {"username": u.username, "email": u.email}
            return None

        def add(self, user: User) -> None:
            self._users[user.identity] = user

    return InMemoryUserGateway()

