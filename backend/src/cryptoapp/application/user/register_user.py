from dataclasses import dataclass

from cryptoapp.application.common.publisher import Publisher, SendActivationEmail
from cryptoapp.application.common.transaction_manager import TransactionManager
from cryptoapp.application.interfaces.generator import ActivationGenerator
from cryptoapp.application.interfaces.sender import EmailSender
from cryptoapp.domain.entities.user.factory import UserFactory


@dataclass(frozen=True, slots=True, eq=True)
class CreateUserDTO:
    username: str
    email: str
    password: str


class RegisterInteractor:
    def __init__(
        self,
        user_factory: UserFactory,
        tr_manager: TransactionManager,
        notification_sender: EmailSender,
        generator: ActivationGenerator,
        publisher: Publisher,
    ):
        self.user_factory = user_factory
        self.tr_manager = tr_manager
        self.notification_service = notification_sender
        self.generator = generator
        self.publisher = publisher

    async def __call__(self, data: CreateUserDTO) -> int:
        user = await self.user_factory.create(
            username=data.username,
            email=data.email,
            password=data.password,
            user_id=None,
        )

        await self.tr_manager.commit()

        url = await self.generator.generate_url(user_id=user.identity)

        await self.publisher.publish_email_task(
            SendActivationEmail(
                email=data.email,
                username=data.username,
                url=url,
            )
        )

        return user.identity
