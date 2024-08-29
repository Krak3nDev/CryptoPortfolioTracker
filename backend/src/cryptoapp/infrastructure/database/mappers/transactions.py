from sqlalchemy.dialects.postgresql import Insert

from cryptoapp.application.interfaces.gateways.transaction import TransactionGateway
from cryptoapp.infrastructure.database.mappers.base import SessionInitializer
from cryptoapp.infrastructure.database.models import TransactionDB
from cryptoapp.infrastructure.dto.data import TransactionDTO


class TransactionMapper(SessionInitializer, TransactionGateway):
    async def add(self, transaction: TransactionDTO) -> None:
        statement = Insert(TransactionDB).values(
            user_id=transaction.user_id,
            quantity=transaction.quantity,
            price_per_unit=transaction.price_per_unit,
            transaction_type=transaction.t_type,
            transaction_dte=transaction.transaction_date,
        )
        await self.session.execute(statement)
