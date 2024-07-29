from dataclasses import replace

from cryptoapp.application.common.exceptions import UserAlreadyExistsError
from cryptoapp.application.common.interactor import Interactor
from cryptoapp.application.dto.user import BasicUserDTO, CreateUserDTO
from cryptoapp.application.interfaces.generator import ActivationGenerator
from cryptoapp.application.interfaces.hasher import IPasswordHasher
from cryptoapp.application.interfaces.repositories.user import UserRepo
from cryptoapp.application.interfaces.sender import INotificationSender
from cryptoapp.application.interfaces.uow import UoW


class RegisterInteractor(Interactor[CreateUserDTO, BasicUserDTO]):
    def __init__(
        self,
        user_repo: UserRepo,
        hash_service: IPasswordHasher,
        uow: UoW,
        notification_sender: INotificationSender,
        generator: ActivationGenerator,
    ):
        self.user_repo = user_repo
        self.hash_service = hash_service
        self.uow = uow
        self.notification_service = notification_sender
        self.generator = generator

    async def __call__(self, data: CreateUserDTO) -> BasicUserDTO:
        user_exist = await self.user_repo.check_user_data_unique(data.username, data.email)

        if user_exist:
            raise UserAlreadyExistsError(data.username)

        hashed_password = self.hash_service.hash(data.password)
        user_data = replace(data, password=hashed_password)
        user = await self.user_repo.create_user(user_data)

        await self.uow.commit()
        url = self.generator.generate(user_id=user.user_id)
        await self.notification_service.send_notification(
            recipient=data.email,
            template_name="email.html",
            subject="Action Required: Confirm Your Email Address",
            data={
                "name": data.full_name,
                "activation_url": url,
            },
        )

        return user
