from abc import abstractmethod
from typing import Protocol


class ActivationGenerator(Protocol):
    @abstractmethod
    async def generate_url(self, user_id: int) -> str:
        pass
