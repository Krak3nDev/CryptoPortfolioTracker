import asyncio
from email.mime.text import MIMEText
from pathlib import Path
from string import Template
from types import TracebackType
from typing import Dict, Optional, Type

import aiosmtplib
from cryptoapp.application.interfaces.sender import INotificationSender
from cryptoapp.config import EmailConfig, load_config
from cryptoapp.infrastructure.services.sender.utils import init_smtp


class EmailSender(INotificationSender):
    def __init__(
        self, config: EmailConfig, smtp_client: aiosmtplib.SMTP, templates_dir: Path
    ) -> None:
        self.config = config
        self.smtp_client = smtp_client
        self.templates_dir = templates_dir

    def load_template(self, template_name: str) -> Template:
        template_path = self.templates_dir / template_name
        with open(template_path, "r", encoding="utf-8") as file:
            return Template(file.read())

    async def send_notification(
        self,
        recipient: str,
        template_name: str,
        subject: str,
        data: Dict[str, int | str],
    ) -> str:
        template = self.load_template(template_name)

        formatted_template = template.substitute(data)

        msg = MIMEText(formatted_template, "html")
        msg["From"] = self.config.sender_email
        msg["To"] = recipient
        msg["Subject"] = subject

        await self.smtp_client.send_message(msg)
        return "The message was sent successfully!"

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        if self.smtp_client.is_connected:
            await self.smtp_client.quit()


async def main() -> None:
    config = load_config()
    smtp_client = await init_smtp(config.email_data)
    email_sender = EmailSender(config.email_data, smtp_client, Path("templates"))
    response = await email_sender.send_notification(
        recipient="insta5441@gmail.com",
        template_name="email.html",
        subject="Action Required: Confirm Your Email Address",
        data={
            "name": "Scotty",
            "activation_url": "123",
        },
    )
    print(response)


if __name__ == "__main__":
    asyncio.run(main())
