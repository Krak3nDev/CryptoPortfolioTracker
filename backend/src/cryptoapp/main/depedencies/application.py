from pathlib import Path

import aiosmtplib
from backend.src.cryptoapp.application.interfaces.repositories.user import UserRepo
from dishka import Provider, Scope, provide

from cryptoapp.application.activation import ActivationInteractor
from cryptoapp.application.get_user_info import GetUserInformationInteractor
from cryptoapp.application.interfaces.repositories.user import UserGateway
from cryptoapp.application.login import LoginInteractor
from cryptoapp.application.register_user import RegisterInteractor
from cryptoapp.config import Config
from cryptoapp.infrastructure.database.mappers.user import UserDataMapper
from cryptoapp.infrastructure.services.auth import AuthService
from cryptoapp.infrastructure.services.committer import SQLAlchemyCommitter
from cryptoapp.infrastructure.services.generator import UrlGenerator
from cryptoapp.infrastructure.services.identifier_service import JWTUserIdentifier
from cryptoapp.infrastructure.services.jwt_service import JWTService
from cryptoapp.infrastructure.services.password_hasher import PasswordHasher
from cryptoapp.infrastructure.services.sender.email_sender import EmailSender
from cryptoapp.infrastructure.services.sender.utils import init_smtp


class ApplicationProvider(Provider):
    @provide(scope=Scope.APP)
    def get_hasher(self) -> PasswordHasher:
        return PasswordHasher()

    @provide(scope=Scope.REQUEST)
    async def get_user_mapper(self, committer: SQLAlchemyCommitter) -> UserDataMapper:
        return UserDataMapper(committer.session)

    @provide(scope=Scope.APP)
    async def get_smtp(self, config: Config) -> aiosmtplib.SMTP:
        return await init_smtp(config.email_data)  # type: ignore

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
    def get_generator(self, jwt: JWTService) -> UrlGenerator:
        return UrlGenerator(jwt)

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
    def get_jwt_service(self, config: Config) -> JWTService:
        return JWTService(
            private_key=config.auth_jwt.private_key_path.read_text(),
            public_key=config.auth_jwt.public_key_path.read_text(),
            algorithm=config.auth_jwt.algorithm,
            access_token_expire_minutes=config.auth_jwt.access_token_expire_minutes,
        )

    @provide(scope=Scope.REQUEST)
    async def auth_service(
        self, user_repo: UserRepo, hasher: PasswordHasher
    ) -> AuthService:
        return AuthService(user_repo, hasher)

    @provide(scope=Scope.APP)
    def get_login_interactor(self, auth: AuthService) -> LoginInteractor:
        return LoginInteractor(auth=auth)

    @provide(scope=Scope.APP)
    def get_identifier(self) -> JWTUserIdentifier:
        return JWTUserIdentifier()

    @provide(scope=Scope.REQUEST)
    def get_user_info_interactor(
        self, user_repo: UserDataMapper, identifier: JWTUserIdentifier
    ) -> GetUserInformationInteractor:
        return GetUserInformationInteractor(user_repo=user_repo, identifier=identifier)

    @provide(scope=Scope.REQUEST)
    def get_activation_interactor(
        self, committer: SQLAlchemyCommitter, user_repo: UserDataMapper, identifier: JWTUserIdentifier
    ) -> ActivationInteractor:
        return ActivationInteractor(committer=committer, user_repo=user_repo, identifier=identifier)
