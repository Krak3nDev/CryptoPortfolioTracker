from abc import abstractmethod
from typing import Protocol

from cryptoapp.domain.entities.portfolio.portfolio import (
    Portfolio,
    PortfolioId,
)
from cryptoapp.domain.entities.user.user import UserId


class PortfolioRepository(Protocol):
    @abstractmethod
    async def by_identity(
        self, portfolio_id: PortfolioId, user_id: UserId
    ) -> Portfolio | None:
        raise NotImplementedError

    @abstractmethod
    async def is_exists(
        self, portfolio_id: PortfolioId, user_id: UserId
    ) -> bool:
        raise NotImplementedError

    @abstractmethod
    def add(self, portfolio: Portfolio) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, portfolio: Portfolio) -> None:
        raise NotImplementedError
