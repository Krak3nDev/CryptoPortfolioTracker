from dataclasses import dataclass

from cryptoapp.application.common.id_provider import IdProvider
from cryptoapp.application.common.transaction_manager import TransactionManager
from cryptoapp.domain.entities.portfolio.portfolio import PortfolioId
from cryptoapp.domain.entities.portfolio.repository import PortfolioRepository
from cryptoapp.domain.entities.transaction.transaction import TransactionId
from cryptoapp.domain.entities.user.user import UserId
from cryptoapp.domain.exceptions import EntityNotFound


@dataclass
class DeleteTransactionRequest:
    portfolio_id: int
    transaction_id: int


class DeleteTransaction:
    def __init__(
        self,
        portfolio_gateway: PortfolioRepository,
        identity_provider: IdProvider,
        transaction_manager: TransactionManager,
    ):
        self._portfolio_gateway = portfolio_gateway
        self._identity_provider = identity_provider
        self._tr_manager = transaction_manager

    async def __call__(self, data: DeleteTransactionRequest) -> None:
        user_id = await self._identity_provider.get_current_user_id()

        portfolio = await self._portfolio_gateway.by_identity(
            portfolio_id=PortfolioId(_value=data.portfolio_id),
            user_id=UserId(user_id),
        )

        if not portfolio:
            raise EntityNotFound(
                field_name="Portfolio", value=data.portfolio_id
            )

        portfolio.remove_transaction(
            transaction_id=TransactionId(_value=data.transaction_id)
        )

        await self._tr_manager.commit()
