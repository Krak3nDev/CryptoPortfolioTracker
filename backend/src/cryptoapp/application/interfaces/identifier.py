from abc import abstractmethod
from typing import Dict, Protocol


class UserIdentifier(Protocol):
    @abstractmethod
    def get_user_id(self, data: Dict[str, str | int]) -> int: ...
