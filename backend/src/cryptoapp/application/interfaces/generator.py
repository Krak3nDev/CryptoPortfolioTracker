from abc import abstractmethod
from typing import Protocol


class ActivationGenerator(Protocol):
    @abstractmethod
    def generate(self, user_id: int) -> str:
        pass
