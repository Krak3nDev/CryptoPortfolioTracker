from cryptoapp.domain.entities.portfolio.portfolio import PortfolioId
from cryptoapp.domain.entities.transaction.repository import (
    TransactionRepository,
)
from cryptoapp.domain.entities.transaction.transaction import (
    Transaction,
    TransactionId,
)
from cryptoapp.domain.entities.user.user import UserId
from cryptoapp.domain.exceptions import EntityNotFound


async def get_transaction_with_ownership_check(
    transaction_repository: TransactionRepository,
    transaction_id: int,
    user_id: int,
    portfolio_id: int,
) -> Transaction:
    transaction = await transaction_repository.by_identity(
        transaction_id=TransactionId(_value=transaction_id),
        portfolio_id=PortfolioId(_value=portfolio_id),
        user_id=UserId(user_id),
    )

    if not transaction:
        raise EntityNotFound(field_name="Transaction", value=transaction_id)

    return transaction
