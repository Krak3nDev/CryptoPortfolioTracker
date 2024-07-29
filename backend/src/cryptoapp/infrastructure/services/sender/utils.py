from aiosmtplib import SMTP
from cryptoapp.config import EmailConfig


async def init_smtp(config: EmailConfig) -> SMTP:
    smtp_client = SMTP(
        hostname=config.smtp_server,
        port=config.smtp_port,
        use_tls=True,
    )
    await smtp_client.connect()

    await smtp_client.login(config.sender_email, config.app_password)
    return smtp_client
