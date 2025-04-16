from sqlalchemy import select

from cryptoapp.domain.entities.portfolio.portfolio import PortfolioId
from cryptoapp.domain.entities.transaction.repository import (
    TransactionRepository,
)
from cryptoapp.domain.entities.transaction.transaction import (
    Transaction,
    TransactionId,
)
from cryptoapp.domain.entities.user.user import UserId
from cryptoapp.infrastructure.persistence.gateways.base import (
    SessionInitializer,
)
from cryptoapp.infrastructure.persistence.tables import (
    portfolios_table,
    transactions_table,
)


class TransactionMapper(TransactionRepository, SessionInitializer):
    def add(self, transaction: Transaction) -> None:
        self._session.add(transaction)

    async def delete(self, transaction: Transaction) -> None:
        await self._session.delete(transaction)

    async def by_identity(
        self,
        transaction_id: TransactionId,
        portfolio_id: PortfolioId,
        user_id: UserId,
    ) -> Transaction | None:
        stmt = (
            select(Transaction)
            .where(
                transactions_table.c.transaction_id == transaction_id.value,
                transactions_table.c.portfolio_id == portfolio_id.value,
            )
            .join(
                portfolios_table,
                transactions_table.c.portfolio_id
                == portfolios_table.c.portfolio_id,
            )
            .where(portfolios_table.c.user_id == user_id.value)
        )

        result: Transaction | None = await self._session.scalar(stmt)
        return result
