from abc import abstractmethod

from cryptoapp.domain.entities.portfolio.portfolio import PortfolioId
from cryptoapp.domain.entities.transaction.transaction import (
    Transaction,
    TransactionId,
)
from cryptoapp.domain.entities.user.user import UserId


class TransactionRepository:
    @abstractmethod
    def add(self, transaction: Transaction) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, transaction: Transaction) -> None:
        raise NotImplementedError

    @abstractmethod
    async def by_identity(
        self,
        transaction_id: TransactionId,
        portfolio_id: PortfolioId,
        user_id: UserId,
    ) -> Transaction | None:
        raise NotImplementedError
