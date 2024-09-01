from cryptoapp.application.common.interactor import Interactor
from cryptoapp.application.interfaces.committer import Committer
from cryptoapp.application.interfaces.gateways.transaction import TransactionGateway


class DeleteTransaction(Interactor[int, None]):
    def __init__(
        self,
        transaction_gateway: TransactionGateway,
        committer: Committer,
    ) -> None:
        self.transaction_gateway = transaction_gateway
        self.commiter = committer

    async def __call__(self, transaction_id: int) -> None:
        await self.transaction_gateway.delete(transaction_id=transaction_id)
        await self.commiter.commit()
