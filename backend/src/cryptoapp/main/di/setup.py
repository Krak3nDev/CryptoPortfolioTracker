from dishka import AsyncContainer, make_async_container
from taskiq import AsyncBroker
from taskiq_aio_pika import AioPikaBroker

from cryptoapp.main.config import (
    CoinMarketCapConfig,
    Config,
    DbConfig,
    EmailConfig,
    RedisConfig,
    S3MinioConfig,
    UrlConfig,
)
from cryptoapp.main.di import providers


def setup_ioc_container(config: Config, broker: AsyncBroker) -> AsyncContainer:
    container = make_async_container(
        *providers,
        context={
            Config: config,
            RedisConfig: config.redis_config,
            UrlConfig: config.url_config,
            EmailConfig: config.email_config,
            DbConfig: config.db,
            S3MinioConfig: config.minio,
            CoinMarketCapConfig: config.coinmarketcap,
            AioPikaBroker: broker,
        },
    )
    return container
