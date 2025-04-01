from sqlalchemy import select

from cryptoapp.domain.entities.portfolio.gateway import PortfolioGateway
from cryptoapp.domain.entities.portfolio.portfolio import Portfolio, PortfolioId
from cryptoapp.domain.entities.user.user import UserId
from cryptoapp.infrastructure.persistence.gateways.base import SessionInitializer
from cryptoapp.infrastructure.persistence.tables import portfolios_table


class PortfolioMapper(SessionInitializer, PortfolioGateway):
    async def by_identity(
        self, portfolio_id: PortfolioId, user_id: UserId
    ) -> Portfolio | None:
        stmt = select(Portfolio).where(
            portfolios_table.c.user_id == user_id.value,
            portfolios_table.c.portfolio_id == portfolio_id.value,
        )
        result = await self._session.scalar(stmt)
        return result

    def add(self, portfolio: Portfolio) -> None:
        self._session.add(portfolio)

    async def delete(self, portfolio: Portfolio) -> None:
        await self._session.delete(portfolio)
