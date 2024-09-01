from fastapi import APIRouter

from cryptoapp.application.crypto_transaction import CryptoTransactionInteractor
from cryptoapp.application.potrfolio.delete import DeleteTransaction
from cryptoapp.presentation.schemas.common import Transaction

portfolio_router = APIRouter(prefix="/portfolio", tags=["portfolio"])


@portfolio_router.post("/transactions/")
async def create_transaction(
    transaction: Transaction, transaction_interactor: CryptoTransactionInteractor
) -> None:
    await transaction_interactor(transaction=transaction.to_dto())


@portfolio_router.delete("/{transaction_id}")
async def delete_crypto_from_portfolio(
    transaction_id: int, delete_interactor: DeleteTransaction
) -> None:
    await delete_interactor(transaction_id=transaction_id)
