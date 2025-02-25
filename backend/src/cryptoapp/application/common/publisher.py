from abc import abstractmethod
from dataclasses import dataclass
from typing import Protocol


@dataclass(slots=True, eq=True)
class SendActivationEmail:
    email: str
    username: str
    url: str


class Publisher(Protocol):
    @abstractmethod
    async def publish_email_task(self, event: SendActivationEmail) -> None: ...
