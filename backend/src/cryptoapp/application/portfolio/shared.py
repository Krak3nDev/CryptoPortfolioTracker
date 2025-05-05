from cryptoapp.domain.entities.portfolio.portfolio import (
    Portfolio,
    PortfolioId,
)
from cryptoapp.domain.entities.portfolio.repository import PortfolioRepository
from cryptoapp.domain.entities.user.user import UserId
from cryptoapp.domain.exceptions import EntityNotFound


async def get_portfolio_with_ownership_check(
    portfolio_repository: PortfolioRepository, user_id: int, portfolio_id: int
) -> Portfolio:
    portfolio = await portfolio_repository.by_identity(
        portfolio_id=PortfolioId(_value=portfolio_id),
        user_id=UserId(user_id),
    )

    if not portfolio:
        raise EntityNotFound(field_name="Portfolio", value=portfolio_id)

    return portfolio
