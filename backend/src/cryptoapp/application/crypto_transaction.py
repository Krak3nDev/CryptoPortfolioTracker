from cryptoapp.application.common.interactor import Interactor
from cryptoapp.application.interfaces.gateways.transaction import TransactionGateway
from cryptoapp.infrastructure.dto.data import TransactionDTO


class CryptoTransactionInteractor(Interactor[TransactionDTO, None]):
    def __init__(self, transaction_gateway: TransactionGateway):
        self.transaction_gateway = transaction_gateway

    def __call__(self, transaction: TransactionDTO) -> None:
        ...
