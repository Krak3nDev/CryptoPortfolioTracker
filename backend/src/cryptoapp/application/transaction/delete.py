from dataclasses import dataclass

from cryptoapp.application.common.id_provider import IdProvider
from cryptoapp.application.common.transaction_manager import TransactionManager
from cryptoapp.application.transaction.shared import (
    get_transaction_with_ownership_check,
)
from cryptoapp.domain.entities.transaction.repository import (
    TransactionRepository,
)


@dataclass
class DeleteTransactionRequest:
    portfolio_id: int
    transaction_id: int


class DeleteTransaction:
    def __init__(
        self,
        transaction_repository: TransactionRepository,
        identity_provider: IdProvider,
        transaction_manager: TransactionManager,
    ):
        self._transaction_repository = transaction_repository
        self._identity_provider = identity_provider
        self._tr_manager = transaction_manager

    async def __call__(self, data: DeleteTransactionRequest) -> None:
        user_id = await self._identity_provider.get_current_user_id()

        transaction = await get_transaction_with_ownership_check(
            transaction_repository=self._transaction_repository,
            transaction_id=data.transaction_id,
            portfolio_id=data.portfolio_id,
            user_id=user_id,
        )
        await self._transaction_repository.delete(transaction)

        await self._tr_manager.commit()
