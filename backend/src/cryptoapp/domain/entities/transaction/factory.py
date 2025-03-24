from dataclasses import dataclass
from decimal import Decimal

from cryptoapp.domain.entities.transaction.gateway import TransactionGateway
from cryptoapp.domain.entities.transaction.transaction import (
    TransactionType,
    Transaction,
    AssetId,
    TransactionId,
)
from cryptoapp.domain.exceptions import AssetNotFound


@dataclass
class CreateTransactionData:
    asset_id: int
    quantity: Decimal
    price: Decimal | None
    transaction_type: TransactionType
    note: str | None
    fee: Decimal | None


class TransactionFactory:
    def __init__(self, transaction_gateway: TransactionGateway):
        self._transaction_gateway = transaction_gateway

    async def create(self, data: CreateTransactionData) -> Transaction:
        asset_id = data.asset_id

        if not await self._transaction_gateway.asset_exist(asset_id):
            raise AssetNotFound(asset_id)

        return Transaction(
            _identity=TransactionId(None),
            _asset_id=AssetId(asset_id),
            _quantity=data.quantity,
            _price=data.price,
            _transaction_type=data.transaction_type,
            _note=data.note,
            _fee=data.fee,
        )
