from fastapi import APIRouter

from cryptoapp.application.crypto_transaction import CryptoTransactionInteractor
from cryptoapp.presentation.schemas.common import Transaction

portfolio_router = APIRouter(prefix="/portfolio", tags=["portfolio"])


@portfolio_router.post("/transactions/")
async def create_transaction(
    transaction: Transaction, transaction_interactor: CryptoTransactionInteractor
) -> None:
    await transaction_interactor(transaction=transaction.to_dto())
