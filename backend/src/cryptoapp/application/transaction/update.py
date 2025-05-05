from dataclasses import dataclass
from decimal import Decimal

from cryptoapp.application.common.id_provider import IdProvider
from cryptoapp.application.common.transaction_manager import TransactionManager
from cryptoapp.application.transaction.shared import (
    get_transaction_with_ownership_check,
)
from cryptoapp.domain.entities.transaction.repository import (
    TransactionRepository,
)


@dataclass
class UpdateTransactionRequest:
    transaction_id: int
    portfolio_id: int
    quantity: Decimal | None
    price: Decimal | None
    note: str | None
    fee: Decimal | None


class UpdateTransaction:
    def __init__(
        self,
        id_provider: IdProvider,
        transaction_repository: TransactionRepository,
        tr_manager: TransactionManager,
    ):
        self._id_provider = id_provider
        self._transaction_repository = transaction_repository
        self._tr_manager = tr_manager

    async def __call__(self, data: UpdateTransactionRequest) -> None:
        user_id = await self._id_provider.get_current_user_id()

        transaction = await get_transaction_with_ownership_check(
            transaction_repository=self._transaction_repository,
            transaction_id=data.transaction_id,
            portfolio_id=data.portfolio_id,
            user_id=user_id,
        )

        transaction.update_transaction(
            quantity=data.quantity,
            price=data.price,
            note=data.note,
            fee=data.fee,
        )

        await self._tr_manager.commit()
