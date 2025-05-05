import logging
from dataclasses import dataclass
from decimal import Decimal

from cryptoapp.application.common.id_provider import IdProvider
from cryptoapp.application.common.transaction_manager import TransactionManager
from cryptoapp.application.interfaces.asset_gateway import AssetGateway
from cryptoapp.domain.entities.transaction.transaction import (
    TransactionType,
)
from cryptoapp.domain.exceptions import EntityNotFound
from cryptoapp.domain.services.transaction import (
    CreateTransactionData,
    TransactionService,
)


@dataclass
class TransactionCreationRequest:
    asset_id: int
    portfolio_id: int
    quantity: Decimal
    price: Decimal | None
    transactionType: TransactionType
    note: str | None
    fee: Decimal | None


class CreateTransaction:
    def __init__(
        self,
        transaction_service: TransactionService,
        asset_gateway: AssetGateway,
        transaction_manager: TransactionManager,
        identity_provider: IdProvider,
    ):
        self._asset_gateway = asset_gateway
        self._transaction_service = transaction_service
        self._tr_manager = transaction_manager
        self._identity_provider = identity_provider

    async def __call__(self, data: TransactionCreationRequest) -> int:
        user_id = await self._identity_provider.get_current_user_id()

        if not await self._asset_gateway.asset_exist(data.asset_id):
            raise EntityNotFound(field_name="Asset", value=data.asset_id)

        transaction = await self._transaction_service.create(
            data=CreateTransactionData(
                user_id=user_id,
                asset_id=data.asset_id,
                note=data.note,
                transaction_type=data.transactionType,
                quantity=data.quantity,
                price=data.price,
                fee=data.fee,
                portfolio_id=data.portfolio_id,
            )
        )

        logging.info(data.portfolio_id)

        await self._tr_manager.commit()

        return transaction.identity.value
