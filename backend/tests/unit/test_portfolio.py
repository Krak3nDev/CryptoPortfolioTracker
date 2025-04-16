import pytest
from cryptoapp.domain.entities.portfolio.portfolio import Portfolio
from cryptoapp.domain.entities.user.user import UserId


@pytest.fixture
def portfolio():
    return Portfolio.create(
        portfolio_id=None,
        user_id=100,
        name="My Portfolio",
        avatar="avatar_url",
    )


def test_portfolio_creation(portfolio):
    assert portfolio.identity._value is None
    assert portfolio._user_id == UserId(100)
    assert portfolio.name == "My Portfolio"
    assert portfolio.avatar == "avatar_url"


