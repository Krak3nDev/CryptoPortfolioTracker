from abc import abstractmethod
from typing import Protocol

from cryptoapp.domain.entities.transaction.transaction import AssetId


class TransactionGateway(Protocol):
    @abstractmethod
    async def asset_exist(self, asset_id: AssetId) -> bool:
        raise NotImplementedError
