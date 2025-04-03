from dataclasses import dataclass
from decimal import Decimal

from cryptoapp.application.common.id_provider import IdProvider
from cryptoapp.application.common.transaction_manager import TransactionManager
from cryptoapp.application.interfaces.asset_gateway import AssetGateway
from cryptoapp.domain.entities.portfolio.portfolio import PortfolioId
from cryptoapp.domain.entities.portfolio.repository import PortfolioRepository
from cryptoapp.domain.entities.transaction.transaction import (
    CreateTransactionData,
    TransactionType,
)
from cryptoapp.domain.entities.user.user import UserId
from cryptoapp.domain.exceptions import EntityNotFound


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
        portfolio_repository: PortfolioRepository,
        asset_gateway: AssetGateway,
        transaction_manager: TransactionManager,
        identity_provider: IdProvider,
    ):
        self._portfolio_repository = portfolio_repository
        self._asset_gateway = asset_gateway
        self._tr_manager = transaction_manager
        self._identity_provider = identity_provider

    async def __call__(self, data: TransactionCreationRequest) -> int:
        user_id = await self._identity_provider.get_current_user_id()

        if not self._asset_gateway.asset_exist(data.asset_id):
            raise EntityNotFound(field_name="Asset", value=data.asset_id)

        portfolio = await self._portfolio_repository.by_identity(
            portfolio_id=PortfolioId(data.portfolio_id),
            user_id=UserId(user_id),
        )

        if not portfolio:
            raise EntityNotFound(
                field_name="Portfolio", value=data.portfolio_id
            )

        transaction_id = portfolio.add_transaction(
            data=CreateTransactionData(
                asset_id=data.asset_id,
                note=data.note,
                transaction_type=data.transactionType,
                quantity=data.quantity,
                price=data.price,
                fee=data.fee,
            )
        )

        await self._tr_manager.commit()

        return transaction_id.value
