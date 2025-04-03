import pytest

from cryptoapp.domain.entities.user.factory import UserFactory
from cryptoapp.domain.entities.user.user import User
from cryptoapp.domain.exceptions import UserAlreadyExistsError
from cryptoapp.infrastructure.services.password_hasher import Hasher


@pytest.fixture(scope="function")
def password_hasher():
    return Hasher()

@pytest.fixture
def user_factory(user_gateway, password_hasher):
    return UserFactory(user_gateway, password_hasher)


@pytest.mark.asyncio
async def test_create_user_success(user_factory):
    username = "new_user"
    email = "new_user@example.com"
    password = "secret"
    user_id = 10

    user = await user_factory.create(username, email, password, user_id)

    assert user.username == username
    assert user.email == email
    assert user.identity.value == user_id
    assert user.is_active is False
    assert user.hashed_password != password


@pytest.mark.asyncio
async def test_create_user_username_taken(user_factory, user_gateway):
    existing_user = User.create(
        user_id=1,
        email="another@example.com",
        hashed_password="hashed_pwd",
        username="busy_username"
    )
    user_gateway.add(existing_user)

    with pytest.raises(UserAlreadyExistsError) as exc_info:
        await user_factory.create(
            username="busy_username",
            email="some_new@example.com",
            password="secret",
            user_id=2
        )

    exc = exc_info.value
    assert exc.username == "busy_username"
    assert exc.email is None


@pytest.mark.asyncio
async def test_create_user_email_taken(user_factory, user_gateway):
    existing_user = User.create(
        user_id=3,
        email="busy@example.com",
        hashed_password="hashed_pwd",
        username="free_username"
    )
    user_gateway.add(existing_user)

    with pytest.raises(UserAlreadyExistsError) as exc_info:
        await user_factory.create(
            username="totally_free",
            email="busy@example.com",
            password="secret",
            user_id=4
        )

    exc = exc_info.value
    assert exc.username is None
    assert exc.email == "busy@example.com"


@pytest.mark.asyncio
async def test_create_user_username_and_email_taken(user_factory, user_gateway):
    existing_user = User.create(
        user_id=5,
        email="taken@example.com",
        hashed_password="hashed_pwd",
        username="taken_username"
    )
    user_gateway.add(existing_user)

    with pytest.raises(UserAlreadyExistsError) as exc_info:
        await user_factory.create(
            username="taken_username",
            email="taken@example.com",
            password="secret",
            user_id=6
        )

    exc = exc_info.value
    assert exc.username == "taken_username"
    assert exc.email == "taken@example.com"