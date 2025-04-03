from dataclasses import dataclass
from decimal import Decimal

from cryptoapp.application.common.id_provider import IdProvider
from cryptoapp.application.common.transaction_manager import TransactionManager
from cryptoapp.domain.entities.portfolio.portfolio import PortfolioId
from cryptoapp.domain.entities.portfolio.repository import PortfolioRepository
from cryptoapp.domain.entities.transaction.transaction import TransactionId
from cryptoapp.domain.entities.user.user import UserId
from cryptoapp.domain.exceptions import EntityNotFound


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
        portfolio_repository: PortfolioRepository,
        tr_manager: TransactionManager,
    ):
        self._id_provider = id_provider
        self._portfolio_repository = portfolio_repository
        self._tr_manager = tr_manager

    async def __call__(self, data: UpdateTransactionRequest) -> None:
        user_id = await self._id_provider.get_current_user_id()

        portfolio = await self._portfolio_repository.by_identity(
            portfolio_id=PortfolioId(data.portfolio_id),
            user_id=UserId(user_id),
        )

        if not portfolio:
            raise EntityNotFound(
                field_name="Portfolio", value=data.portfolio_id
            )

        portfolio.update_transaction(
            transaction_id=TransactionId(data.transaction_id),
            quantity=data.quantity,
            price=data.price,
            note=data.note,
        )

        await self._tr_manager.commit()
