
from cryptoapp.domain.entities.transaction.gateway import TransactionGateway
from cryptoapp.domain.entities.transaction.transaction import (
    CreateTransactionData,
    Transaction,
)
from cryptoapp.domain.exceptions import EntityNotFound


class TransactionFactory:
    def __init__(self, transaction_gateway: TransactionGateway):
        self._transaction_gateway = transaction_gateway

    async def create(self, data: CreateTransactionData) -> Transaction:
        if not await self._transaction_gateway.asset_exist(data.asset_id):
            raise EntityNotFound(field_name="Asset", value=data.asset_id.value)

        return Transaction.create(data=data)
