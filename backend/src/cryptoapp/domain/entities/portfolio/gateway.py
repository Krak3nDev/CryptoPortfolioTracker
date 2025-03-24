from abc import abstractmethod
from typing import Protocol

from cryptoapp.domain.entities.portfolio.portfolio import Portfolio


class PortfolioGateway(Protocol):
    @abstractmethod
    async def by_identity(self, portfolio_id: int, user_id: int) -> Portfolio | None:
        raise NotImplementedError

    @abstractmethod
    def add(self, portfolio: Portfolio) -> None:
        raise NotImplementedError
