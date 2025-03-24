from dataclasses import dataclass

from cryptoapp.application.common.publisher import Publisher, SendActivationEmail
from cryptoapp.application.common.transaction_manager import TransactionManager
from cryptoapp.application.common.validators import validate_length, validate_email
from cryptoapp.application.interfaces.generator import ActivationGenerator
from cryptoapp.application.interfaces.sender import EmailSender
from cryptoapp.domain.entities.user.factory import UserFactory


@dataclass(frozen=True, slots=True, eq=True)
class CreationUserRequest:
    username: str
    email: str
    password: str


USERNAME_LENGTH = 50


def validate_creation_user_data(username: str, email: str) -> None:
    validate_length(max_length=USERNAME_LENGTH, field_name="username", value=username)
    validate_email(value=email)


class RegisterInteractor:
    def __init__(
        self,
        user_factory: UserFactory,
        tr_manager: TransactionManager,
        notification_sender: EmailSender,
        generator: ActivationGenerator,
        publisher: Publisher,
    ):
        self._user_factory = user_factory
        self._tr_manager = tr_manager
        self._notification_service = notification_sender
        self._generator = generator
        self._publisher = publisher

    async def __call__(self, data: CreationUserRequest) -> int:
        validate_creation_user_data(email=data.email, username=data.username)

        user = await self._user_factory.create(
            username=data.username,
            email=data.email,
            password=data.password,
            user_id=None,
        )

        await self._tr_manager.commit()

        url = await self._generator.generate_url(user_id=user.identity)

        await self._publisher.publish_email_task(
            SendActivationEmail(
                email=data.email,
                username=data.username,
                url=url,
            )
        )

        return user.identity
