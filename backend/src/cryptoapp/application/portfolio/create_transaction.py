from dataclasses import dataclass
from decimal import Decimal

from cryptoapp.application.common.id_provider import IdProvider
from cryptoapp.application.common.transaction_manager import TransactionManager
from cryptoapp.domain.entities.portfolio.gateway import PortfolioGateway
from cryptoapp.domain.entities.transaction.factory import (
    TransactionFactory,
    CreateTransactionData,
)
from cryptoapp.domain.entities.transaction.transaction import TransactionType
from cryptoapp.domain.exceptions import PortfolioNotFound


@dataclass
class TransactionCreationRequest:
    asset_id: int
    portfolio_id: int
    quantity: Decimal
    price: Decimal | None
    transactionType: TransactionType
    note: str | None
    fee: Decimal | None


NOTE_LENGTH = 255


class CreateTransaction:
    def __init__(
        self,
        portfolio_gateway: PortfolioGateway,
        factory: TransactionFactory,
        transaction_manager: TransactionManager,
        identity_provider: IdProvider,
    ):
        self._portfolio_gateway = portfolio_gateway
        self._factory = factory
        self._tr_manager = transaction_manager
        self._identity_provider = identity_provider

    async def __call__(self, data: TransactionCreationRequest) -> int:
        user_id = await self._identity_provider.get_current_user_id()

        transaction = await self._factory.create(
            data=CreateTransactionData(
                asset_id=data.asset_id,
                note=data.note,
                transaction_type=data.transactionType,
                quantity=data.quantity,
                price=data.price,
                fee=data.fee,
            )
        )

        portfolio = await self._portfolio_gateway.by_identity(
            portfolio_id=data.portfolio_id, user_id=user_id
        )

        if not portfolio:
            raise PortfolioNotFound(portfolio_id=data.portfolio_id)

        portfolio.add_transaction(transaction)

        await self._tr_manager.commit()

        return transaction.identity
