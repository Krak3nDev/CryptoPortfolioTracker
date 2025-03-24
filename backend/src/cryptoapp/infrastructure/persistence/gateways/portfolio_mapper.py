from sqlalchemy import select

from cryptoapp.domain.entities.portfolio.gateway import PortfolioGateway
from cryptoapp.domain.entities.portfolio.portfolio import Portfolio
from cryptoapp.infrastructure.persistence.gateways.base import SessionInitializer
from cryptoapp.infrastructure.persistence.tables import portfolios_table


class PortfolioMapper(SessionInitializer, PortfolioGateway):
    async def by_identity(self, portfolio_id: int, user_id: int) -> Portfolio | None:
        stmt = select(Portfolio).where(
            portfolios_table.c.user_id == user_id,
            portfolios_table.c.portfolio_id == portfolio_id,
        )
        result = await self._session.scalar(stmt)
        return result

    def add(self, portfolio: Portfolio) -> None:
        self._session.add(portfolio)
