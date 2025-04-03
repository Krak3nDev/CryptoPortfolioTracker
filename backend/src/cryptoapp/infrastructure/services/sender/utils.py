from contextlib import asynccontextmanager
from typing import AsyncIterator

import aiosmtplib

from cryptoapp.main.config import EmailConfig


@asynccontextmanager
async def smtp_client_context(
    config: EmailConfig,
) -> AsyncIterator[aiosmtplib.SMTP]:
    smtp_client = aiosmtplib.SMTP(
        hostname=config.smtp_server,
        port=config.smtp_port,
        use_tls=config.tls,
        start_tls=False,
    )
    await smtp_client.connect()
    try:
        await smtp_client.login(config.sender_email, config.app_password)
        yield smtp_client
    finally:
        if smtp_client.is_connected:
            await smtp_client.quit()
