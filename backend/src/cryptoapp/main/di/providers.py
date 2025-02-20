from pathlib import Path
from typing import AsyncIterable

import aiosmtplib
from dishka import AnyOf, Provider, Scope, from_context, provide
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker
from starlette.requests import Request

from cryptoapp.application.common.id_provider import IdProvider
from cryptoapp.application.common.transaction_manager import TransactionManager
from cryptoapp.application.interfaces.generator import ActivationGenerator
from cryptoapp.application.interfaces.sender import EmailSender
from cryptoapp.application.user.activation import ActivateUserProfileInteractor
from cryptoapp.application.user.register_user import RegisterInteractor
from cryptoapp.domain.entities.user.factory import UserFactory
from cryptoapp.domain.entities.user.gateway import UserGateway
from cryptoapp.domain.entities.user.hasher import PasswordHasher
from cryptoapp.infrastructure.persistence.gateways.user_mapper import UserMapper
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
from cryptoapp.infrastructure.services.generator import UrlGenerator
from cryptoapp.infrastructure.services.password_hasher import Hasher
from cryptoapp.infrastructure.services.sender.email_sender import SMTPEmailSender
from cryptoapp.infrastructure.services.sender.utils import smtp_client_context
from cryptoapp.main.config import Config, DbConfig, EmailConfig, RedisConfig, UrlConfig


class ConfigProvider(Provider):
    config = from_context(Config, scope=Scope.APP)
    redis_config = from_context(RedisConfig, scope=Scope.APP)
    url_config = from_context(UrlConfig, scope=Scope.APP)
    email_config = from_context(EmailConfig, scope=Scope.APP)
    db_config = from_context(DbConfig, scope=Scope.APP)


class InfrastructureServiceProvider(Provider):
    hasher = provide(source=Hasher, provides=PasswordHasher, scope=Scope.APP)
    activation_token_id_provider = provide(
        source=ActivationTokenIdProvider, provides=IdProvider, scope=Scope.REQUEST
    )
    url_generator = provide(
        source=UrlGenerator, provides=ActivationGenerator, scope=Scope.APP
    )

    @provide(scope=Scope.REQUEST)
    def get_activation_token(self, request: Request) -> Activation_Token:
        return get_activation_token(request=request)

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


class DomainServiceProvider(Provider):
    user_factory = provide(source=UserFactory, scope=Scope.REQUEST)


class InteractorProvider(Provider):
    register_interactor = provide(source=RegisterInteractor, scope=Scope.REQUEST)
    user_activation = provide(source=ActivateUserProfileInteractor, scope=Scope.REQUEST)


class MapperProvider(Provider):
    user_mapper = provide(
        source=UserMapper, provides=AnyOf[UserGateway,], scope=Scope.REQUEST
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
