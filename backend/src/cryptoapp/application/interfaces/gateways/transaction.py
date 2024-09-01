from typing import Protocol

from cryptoapp.infrastructure.dto.data import TransactionDTO


class TransactionGateway(Protocol):
    async def add(self, transaction: TransactionDTO) -> None: ...

    async def delete(self, transaction_id: int) -> None: ...
