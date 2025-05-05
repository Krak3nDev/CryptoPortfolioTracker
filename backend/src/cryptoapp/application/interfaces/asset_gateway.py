from abc import abstractmethod
from typing import Protocol


class AssetGateway(Protocol):
    @abstractmethod
    async def asset_exist(self, asset_id: int) -> bool:
        raise NotImplementedError
