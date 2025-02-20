from dataclasses import dataclass

from cryptoapp.application.common.transaction_manager import TransactionManager
from cryptoapp.application.interfaces.generator import ActivationGenerator
from cryptoapp.application.interfaces.sender import EmailSender
from cryptoapp.domain.entities.user.factory import UserFactory


@dataclass
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
    ):
        self.user_factory = user_factory
        self.tr_manager = tr_manager
        self.notification_service = notification_sender
        self.generator = generator

    async def __call__(self, data: CreateUserDTO) -> None:
        user = await self.user_factory.create(
            username=data.username,
            email=data.email,
            password=data.password,
            user_id=None,
        )

        await self.tr_manager.commit()

        url = await self.generator.generate_url(user_id=user.identity)

        await self.notification_service.send_notification(
            recipient=data.email,
            template_name="email.html",
            subject="Action Required: Confirm Your Email Address",
            data={
                "name": data.username,
                "activation_url": url,
            },
        )
