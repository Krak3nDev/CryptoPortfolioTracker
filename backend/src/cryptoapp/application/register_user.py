from dataclasses import replace

from cryptoapp.application.common.exceptions import UserAlreadyExistsError
from cryptoapp.application.common.interactor import Interactor
from cryptoapp.application.interfaces.committer import Committer
from cryptoapp.application.interfaces.gateways.user import UserGateway
from cryptoapp.application.interfaces.generator import ActivationGenerator
from cryptoapp.application.interfaces.hasher import IPasswordHasher
from cryptoapp.application.interfaces.sender import INotificationSender
from cryptoapp.infrastructure.dto.converters import convert_entity_to_dto
from cryptoapp.infrastructure.dto.data import CreateUserDTO, UserDTO


class RegisterInteractor(Interactor[CreateUserDTO, UserDTO]):
    def __init__(
        self,
        user_gateway: UserGateway,
        hash_service: IPasswordHasher,
        committer: Committer,
        notification_sender: INotificationSender,
        generator: ActivationGenerator,
    ):
        self.user_gateway = user_gateway
        self.hash_service = hash_service
        self.committer = committer
        self.notification_service = notification_sender
        self.generator = generator

    async def __call__(self, data: CreateUserDTO) -> UserDTO:
        user_exist = await self.user_gateway.check_data_unique(
            data.username, data.email
        )

        if user_exist:
            raise UserAlreadyExistsError(data.username)

        hashed_password = self.hash_service.hash(data.password)
        user_data = replace(data, password=hashed_password)
        user = await self.user_gateway.add(user_data)

        await self.committer.commit()
        url = self.generator.generate(user_id=user.id)
        await self.notification_service.send_notification(
            recipient=data.email,
            template_name="email.html",
            subject="Action Required: Confirm Your Email Address",
            data={
                "name": data.full_name,
                "activation_url": url,
            },
        )

        return convert_entity_to_dto(user)
