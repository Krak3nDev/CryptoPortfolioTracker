from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from cryptoapp.main.config import Config, DbConfig, EmailConfig, RedisConfig, UrlConfig

from . import providers


def setup_ioc_container(config: Config, app: FastAPI) -> None:
    container = make_async_container(
        *providers,
        context={
            Config: config,
            RedisConfig: config.redis_config,
            UrlConfig: config.url_config,
            EmailConfig: config.email_config,
            DbConfig: config.db,
        },
    )
    setup_dishka(container, app)
