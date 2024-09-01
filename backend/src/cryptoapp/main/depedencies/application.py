from pathlib import Path

import aiosmtplib
from dishka import Provider, Scope, from_context, provide
from fastapi.requests import Request

from cryptoapp.application.potrfolio.delete import DeleteTransaction
from cryptoapp.application.user.activation import ActivationInteractor
from cryptoapp.application.user.get_user_info import GetUserInformationInteractor
from cryptoapp.application.user.register_user import RegisterInteractor
from cryptoapp.config import Config
from cryptoapp.infrastructure.database.mappers.assets import AssetMapper
from cryptoapp.infrastructure.database.mappers.transactions import TransactionMapper
from cryptoapp.infrastructure.database.mappers.users import UserDataMapper
from cryptoapp.infrastructure.dto.data import TokenPayloadDTO
from cryptoapp.infrastructure.services.auth import AuthService
from cryptoapp.infrastructure.services.committer import SQLAlchemyCommitter
from cryptoapp.infrastructure.services.generator import UrlGenerator
from cryptoapp.infrastructure.services.jwt_id_provider import TokenIdProvider
from cryptoapp.infrastructure.services.jwt_service import (
    JwtTokenProcessor,
    get_token_info,
)
from cryptoapp.infrastructure.services.password_hasher import PasswordHasher
from cryptoapp.infrastructure.services.sender.email_sender import EmailSender
from cryptoapp.infrastructure.services.sender.utils import init_smtp


class ApplicationProvider(Provider):
    request = from_context(provides=Request, scope=Scope.REQUEST)

    @provide(scope=Scope.APP)
    def get_hasher(self) -> PasswordHasher:
        return PasswordHasher()

    @provide(scope=Scope.REQUEST)
    async def get_user_mapper(self, committer: SQLAlchemyCommitter) -> UserDataMapper:
        return UserDataMapper(committer.session)

    @provide(scope=Scope.REQUEST)
    async def get_asset_mapper(self, committer: SQLAlchemyCommitter) -> AssetMapper:
        return AssetMapper(committer.session)

    @provide(scope=Scope.REQUEST)
    async def get_transaction_mapper(
        self, committer: SQLAlchemyCommitter
    ) -> TransactionMapper:
        return TransactionMapper(committer.session)

    @provide(scope=Scope.APP)
    async def get_smtp(self, config: Config) -> aiosmtplib.SMTP:
        return await init_smtp(config.email_data)

    @provide(scope=Scope.APP)
    def get_sender(
        self,
        config: Config,
        smtp: aiosmtplib.SMTP,
    ) -> EmailSender:
        templates_dir = Path("src/cryptoapp/infrastructure/services/sender/templates")
        return EmailSender(
            config=config.email_data, smtp_client=smtp, templates_dir=templates_dir
        )

    @provide(scope=Scope.APP)
    def get_generator(self, jwt: JwtTokenProcessor, config: Config) -> UrlGenerator:
        return UrlGenerator(jwt, domain_config=config.domain)

    @provide(scope=Scope.REQUEST)
    async def get_register_service(
        self,
        user_mapper: UserDataMapper,
        hasher: PasswordHasher,
        committer: SQLAlchemyCommitter,
        notification_sender: EmailSender,
        generator: UrlGenerator,
    ) -> RegisterInteractor:
        return RegisterInteractor(
            user_gateway=user_mapper,
            hash_service=hasher,
            committer=committer,
            notification_sender=notification_sender,
            generator=generator,
        )

    @provide(scope=Scope.APP)
    def get_jwt_service(self, config: Config) -> JwtTokenProcessor:
        return JwtTokenProcessor(
            private_key=config.auth_jwt.private_key_path.read_text(),
            public_key=config.auth_jwt.public_key_path.read_text(),
            algorithm=config.auth_jwt.algorithm,
            access_token_expire_minutes=config.auth_jwt.access_token_expire_minutes,
        )

    @provide(scope=Scope.REQUEST)
    async def get_authentication_service(
        self,
        user_gateway: UserDataMapper,
        hasher: PasswordHasher,
        jwt: JwtTokenProcessor,
    ) -> AuthService:
        return AuthService(user_gateway=user_gateway, hasher=hasher, jwt=jwt)

    @provide(scope=Scope.REQUEST)
    def get_token_id_provider(self, token: TokenPayloadDTO) -> TokenIdProvider:
        return TokenIdProvider(token=token)

    @provide(scope=Scope.REQUEST)
    def get_token(
        self, request: Request, token_processor: JwtTokenProcessor
    ) -> TokenPayloadDTO:
        return token_processor.decode_jwt(get_token_info(request))

    @provide(scope=Scope.REQUEST)
    async def get_user_info_interactor(
        self,
        user_gateway: UserDataMapper,
    ) -> GetUserInformationInteractor:
        return GetUserInformationInteractor(user_gateway=user_gateway)

    @provide(scope=Scope.REQUEST)
    async def get_activation_interactor(
        self,
        committer: SQLAlchemyCommitter,
        user_gateway: UserDataMapper,
        id_provider: TokenIdProvider,
    ) -> ActivationInteractor:
        return ActivationInteractor(
            committer=committer, user_gateway=user_gateway, id_provider=id_provider
        )

    @provide(scope=Scope.REQUEST)
    async def get_delete_transaction(
        self, transaction_gateway: TransactionMapper, committer: SQLAlchemyCommitter
    ) -> DeleteTransaction:
        return DeleteTransaction(
            transaction_gateway=transaction_gateway, committer=committer
        )
