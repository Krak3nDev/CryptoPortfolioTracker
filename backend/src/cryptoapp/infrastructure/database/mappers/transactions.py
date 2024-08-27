from cryptoapp.application.interfaces.gateways.transaction import TransactionGateway
from cryptoapp.infrastructure.database.mappers.base import SessionInitializer


class TransactionMapper(SessionInitializer, TransactionGateway):
    ...
