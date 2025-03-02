from dataclasses import dataclass

from cryptoapp.application.interfaces.sender import EmailSender


@dataclass(frozen=True, slots=True, eq=True)
class EmailData:
    email: str
    username: str
    url: str


class SendMailInteractor:
    def __init__(self, notification_sender: EmailSender) -> None:
        self.notification_sender = notification_sender

    async def __call__(self, data: EmailData) -> None:
        await self.notification_sender.send_notification(
            recipient=data.email,
            template_name="email.html",
            subject="Action Required: Confirm Your Email Address",
            data={
                "name": data.username,
                "activation_url": data.url,
            },
        )
