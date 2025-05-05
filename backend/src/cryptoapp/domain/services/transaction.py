from dataclasses import dataclass
from decimal import Decimal

from cryptoapp.domain.entities.portfolio.portfolio import PortfolioId
from cryptoapp.domain.entities.portfolio.repository import PortfolioRepository
from cryptoapp.domain.entities.transaction.repository import (
    TransactionRepository,
)
from cryptoapp.domain.entities.transaction.transaction import (
    CreationData,
    Transaction,
    TransactionType,
)
from cryptoapp.domain.entities.user.user import UserId
from cryptoapp.domain.exceptions import EntityNotFound


@dataclass
class CreateTransactionData:
    user_id: int
    asset_id: int
    portfolio_id: int
    quantity: Decimal
    price: Decimal | None
    transaction_type: TransactionType
    note: str | None
    fee: Decimal | None


class TransactionService:
    def __init__(
        self,
        portfolio_repository: PortfolioRepository,
        transaction_repository: TransactionRepository,
    ):
        self._portfolio_repository = portfolio_repository
        self._transaction_repository = transaction_repository

    async def create(self, data: CreateTransactionData) -> Transaction:
        portfolio = await self._portfolio_repository.is_exists(
            portfolio_id=PortfolioId(data.portfolio_id),
            user_id=UserId(data.user_id),
        )

        if not portfolio:
            raise EntityNotFound(
                field_name="Portfolio", value=data.portfolio_id
            )

        transaction = Transaction.create(
            data=CreationData(
                asset_id=data.asset_id,
                note=data.note,
                transaction_type=data.transaction_type,
                quantity=data.quantity,
                price=data.price,
                fee=data.fee,
                portfolio_id=data.portfolio_id,
            )
        )

        self._transaction_repository.add(transaction)

        return transaction
