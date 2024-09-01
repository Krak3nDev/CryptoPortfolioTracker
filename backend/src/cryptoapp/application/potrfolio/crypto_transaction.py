from cryptoapp.application.common.interactor import (
    Interactor,
)
from cryptoapp.application.interfaces.committer import (
    Committer,
)
from cryptoapp.application.interfaces.gateways.transaction import (
    TransactionGateway,
)
from cryptoapp.infrastructure.dto.data import (
    TransactionDTO,
)


class CryptoTransactionInteractor(Interactor[TransactionDTO, None]):
    def __init__(
        self,
        transaction_gateway: TransactionGateway,
        committer: Committer,
    ) -> None:
        self.transaction_gateway = transaction_gateway
        self.commiter = committer

    async def __call__(self, transaction: TransactionDTO) -> None:
        await self.transaction_gateway.add(transaction=transaction)
        await self.commiter.commit()
