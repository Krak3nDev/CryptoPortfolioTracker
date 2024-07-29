from typing import Dict, Protocol, Union


class INotificationSender(Protocol):
    async def send_notification(
        self,
        recipient: str,
        template_name: str,
        subject: str,
        data: Dict[str, Union[int, str]],
    ) -> str: ...
