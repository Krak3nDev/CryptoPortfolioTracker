from abc import abstractmethod
from typing import Dict, Protocol


class EmailSender(Protocol):
    @abstractmethod
    async def send_notification(
        self,
        recipient: str,
        template_name: str,
        subject: str,
        data: Dict[str, int | str],
    ) -> str: ...
