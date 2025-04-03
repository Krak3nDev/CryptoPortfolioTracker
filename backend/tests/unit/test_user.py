import pytest
from cryptoapp.domain.entities.user.user import UserId
from cryptoapp.domain.exceptions import DomainError


def test_user_creation(user):
    assert user.identity == UserId(1)
    assert user.email == "test@example.com"
    assert user.username == "testuser"
    assert user.hashed_password == "hashed_password"
    assert not user.is_active

def test_user_activation(user):
    user.activate()
    assert user.is_active

def test_user_activate_twice_raises_exception(user):
    user.activate()
    with pytest.raises(DomainError):
        user.activate()
