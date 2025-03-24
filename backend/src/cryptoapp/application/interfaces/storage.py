from abc import abstractmethod
from typing import Protocol


class StorageService(Protocol):
    @abstractmethod
    async def upload_from_bytes(self, data: bytes, file_name: str) -> str:
        raise NotImplementedError
