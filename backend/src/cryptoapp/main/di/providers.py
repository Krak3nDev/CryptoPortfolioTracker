from pathlib import Path
from typing import Annotated, AsyncIterable

from aioboto3 import Session
from aiobotocore.client import AioBaseClient
from httpx import AsyncClient

import aiosmtplib
from dishka import AnyOf, FromComponent, Provider, Scope, from_context, provide
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker
from starlette.requests import Request
from taskiq_aio_pika import AioPikaBroker

from cryptoapp.application.common.id_provider import IdProvider
from cryptoapp.application.common.publisher import Publisher
from cryptoapp.application.common.transaction_manager import TransactionManager
from cryptoapp.application.interfaces.generator import ActivationGenerator
from cryptoapp.application.interfaces.sender import EmailSender
from cryptoapp.application.interfaces.storage import StorageService
from cryptoapp.application.portfolio.create import (
    CreatePortfolio,
)
from cryptoapp.application.portfolio.create_transaction import CreateTransaction
from cryptoapp.application.user.activation import ActivateUserProfileInteractor
from cryptoapp.application.user.login import LoginInteractor
from cryptoapp.application.user.register_user import RegisterInteractor
from cryptoapp.application.user.send_mail import SendMailInteractor
from cryptoapp.domain.entities.portfolio.factory import PortfolioFactory
from cryptoapp.domain.entities.portfolio.gateway import PortfolioGateway
from cryptoapp.domain.entities.transaction.factory import TransactionFactory
from cryptoapp.domain.entities.transaction.gateway import TransactionGateway
from cryptoapp.domain.entities.user.factory import UserFactory
from cryptoapp.domain.entities.user.gateway import UserGateway
from cryptoapp.domain.entities.user.hasher import PasswordHasher
from cryptoapp.infrastructure.persistence.gateways.portfolio_mapper import (
    PortfolioMapper,
)
from cryptoapp.infrastructure.persistence.gateways.session_mapper import SessionGateway
from cryptoapp.infrastructure.persistence.gateways.transaction_mapper import (
    TransactionMapper,
)
from cryptoapp.infrastructure.persistence.gateways.user_mapper import UserMapper
from cryptoapp.infrastructure.persistence.readers.portfolio import PortfolioReader
from cryptoapp.infrastructure.persistence.setup import (
    create_engine,
    create_session_pool,
)
from cryptoapp.infrastructure.persistence.transaction_manager import (
    AlchemyTransactionManager,
)
from cryptoapp.infrastructure.services.activation_token_id_provider import (
    Activation_Token,
    ActivationTokenIdProvider,
    get_activation_token,
)
from cryptoapp.infrastructure.services.auth import Auther
from cryptoapp.infrastructure.services.generator import UrlGenerator
from cryptoapp.infrastructure.services.marcetcap_api.api import CoinMarketCapAPI
from cryptoapp.infrastructure.services.minio import S3Minio
from cryptoapp.infrastructure.services.password_hasher import Hasher
from cryptoapp.infrastructure.services.rabbit_publisher import RabbitPublisher
from cryptoapp.infrastructure.services.sender.email_sender import SMTPEmailSender
from cryptoapp.infrastructure.services.sender.utils import smtp_client_context
from cryptoapp.infrastructure.services.session_id_provider import (
    FastAPISessionIDGetter,
    HTTPIdentityProvider,
    SessionIDGetter,
)
from cryptoapp.infrastructure.services.session_manager import (
    FastAPISessionManager,
    HTTPSessionManager,
)
from cryptoapp.main.config import (
    Config,
    DbConfig,
    EmailConfig,
    RedisConfig,
    UrlConfig,
    S3MinioConfig,
    CoinMarketCapConfig,
)


class ConfigProvider(Provider):
    config = from_context(Config, scope=Scope.APP)
    redis_config = from_context(RedisConfig, scope=Scope.APP)
    url_config = from_context(UrlConfig, scope=Scope.APP)
    email_config = from_context(EmailConfig, scope=Scope.APP)
    db_config = from_context(DbConfig, scope=Scope.APP)
    market_api_config = from_context(CoinMarketCapConfig, scope=Scope.APP)
    minio_config = from_context(S3MinioConfig, scope=Scope.APP)


class ActivationProvider(Provider):
    component = "additional"

    @provide(scope=Scope.REQUEST)
    async def get_user_activation_interactor(
        self,
        identity_provider: ActivationTokenIdProvider,
        user_gateway: Annotated[UserGateway, FromComponent("")],
        transaction_manager: Annotated[TransactionManager, FromComponent("")],
    ) -> ActivateUserProfileInteractor:
        return ActivateUserProfileInteractor(
            identity_provider=identity_provider,
            user_gateway=user_gateway,
            transaction_manager=transaction_manager,
        )

    @provide(scope=Scope.REQUEST)
    def get_activation_token(
        self, request: Annotated[Request, FromComponent("")]
    ) -> Activation_Token:
        return get_activation_token(request=request)

    @provide(scope=Scope.REQUEST)
    def get_activation_token_id_provider(
        self,
        redis: Annotated[Redis, FromComponent("")],
        user_gateway: Annotated[UserGateway, FromComponent("")],
        token: Activation_Token,
    ) -> ActivationTokenIdProvider:
        return ActivationTokenIdProvider(
            redis=redis, token=token, user_gateway=user_gateway
        )


class InfrastructureServiceProvider(Provider):
    broker = from_context(AioPikaBroker, scope=Scope.APP)
    publisher = provide(source=RabbitPublisher, provides=Publisher, scope=Scope.APP)
    hasher = provide(source=Hasher, provides=PasswordHasher, scope=Scope.APP)
    url_generator = provide(
        source=UrlGenerator, provides=ActivationGenerator, scope=Scope.APP
    )

    @provide(scope=Scope.APP)
    async def smtp_client(self, config: EmailConfig) -> AsyncIterable[aiosmtplib.SMTP]:
        async with smtp_client_context(config) as smtp:
            yield smtp

    @provide(scope=Scope.APP, provides=EmailSender)
    def email_sender(
        self, config: EmailConfig, smtp: aiosmtplib.SMTP
    ) -> SMTPEmailSender:
        return SMTPEmailSender(
            config=config,
            smtp_client=smtp,
            templates_dir=Path("cryptoapp/infrastructure/services/sender/templates"),
        )

    http_identity_provider = provide(
        source=HTTPIdentityProvider, provides=IdProvider, scope=Scope.REQUEST
    )
    session_id_getter = provide(
        source=FastAPISessionIDGetter, provides=SessionIDGetter, scope=Scope.REQUEST
    )
    session_mapper = provide(source=SessionGateway, scope=Scope.APP)

    http_session_manager = provide(source=HTTPSessionManager, scope=Scope.APP)
    fastapi_session_manager = provide(source=FastAPISessionManager, scope=Scope.APP)

    auth_manager = provide(source=Auther, scope=Scope.REQUEST)

    minio = provide(
        source=S3Minio, provides=AnyOf[StorageService, S3Minio], scope=Scope.APP
    )

    market_api = provide(source=CoinMarketCapAPI, scope=Scope.APP)

    @provide(scope=Scope.APP)
    async def provide_async_client(self) -> AsyncIterable[AsyncClient]:
        async with AsyncClient() as client:
            yield client

    @provide(scope=Scope.APP)
    def provide_s3_session(self, minio_config: S3MinioConfig) -> Session:
        return Session(
            aws_access_key_id=minio_config.aws_access_key,
            aws_secret_access_key=minio_config.aws_secret_access_key,
        )

    @provide(scope=Scope.APP)
    async def provide_s3(
        self, session: Session, minio_config: S3MinioConfig
    ) -> AsyncIterable[AioBaseClient]:
        async with session.client(
            "s3",
            endpoint_url=minio_config.base_url,
        ) as s3:
            yield s3

    portfolio_reader = provide(PortfolioReader, scope=Scope.REQUEST)


class DomainServiceProvider(Provider):
    user_factory = provide(source=UserFactory, scope=Scope.REQUEST)
    portfolio_factory = provide(source=PortfolioFactory, scope=Scope.REQUEST)
    transaction_factory = provide(source=TransactionFactory, scope=Scope.REQUEST)


class InteractorProvider(Provider):
    send_mail = provide(source=SendMailInteractor, scope=Scope.REQUEST)
    register = provide(source=RegisterInteractor, scope=Scope.REQUEST)
    login = provide(source=LoginInteractor, scope=Scope.REQUEST)
    create_portfolio = provide(source=CreatePortfolio, scope=Scope.REQUEST)
    create_transaction = provide(source=CreateTransaction, scope=Scope.REQUEST)


class MapperProvider(Provider):
    user_mapper = provide(
        source=UserMapper, provides=AnyOf[UserGateway, UserMapper], scope=Scope.REQUEST
    )
    portfolio_mapper = provide(
        source=PortfolioMapper, provides=PortfolioGateway, scope=Scope.REQUEST
    )
    transaction_mapper = provide(
        source=TransactionMapper, provides=TransactionGateway, scope=Scope.REQUEST
    )


class DbProvider(Provider):
    @provide(scope=Scope.APP)
    def engine(self, db_config: DbConfig) -> AsyncEngine:
        return create_engine(db_config)

    @provide(scope=Scope.APP)
    def session_pool(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return create_session_pool(engine)

    @provide(scope=Scope.REQUEST)
    async def session(
        self, session_factory: async_sessionmaker[AsyncSession]
    ) -> AsyncIterable[AsyncSession]:
        async with session_factory() as session:
            yield session

    @provide(scope=Scope.APP)
    def get_redis(self, redis_config: RedisConfig) -> Redis:
        return Redis(
            host=redis_config.host,
            port=redis_config.port,
            password=redis_config.password,
        )

    transaction_manager = provide(
        source=AlchemyTransactionManager,
        provides=TransactionManager,
        scope=Scope.REQUEST,
    )
