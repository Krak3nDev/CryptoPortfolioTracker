from cryptoapp.application.common.exceptions import (
    UserDoesNotExistError,
)
from cryptoapp.application.common.interactor import Interactor
from cryptoapp.application.interfaces.committer import Committer
from cryptoapp.application.interfaces.gateways.user import UserGateway
from cryptoapp.application.interfaces.id_provider import IdProvider


class ActivationInteractor(Interactor[None, None]):
    def __init__(
        self, user_gateway: UserGateway, committer: Committer, id_provider: IdProvider
    ):
        self.user_gateway = user_gateway
        self.committer = committer
        self.id_provider = id_provider

    async def __call__(self, data: None = None) -> None:
        user_id = self.id_provider.get_current_user_id()
        user = await self.user_gateway.get_by_id(user_id)

        if not user:
            raise UserDoesNotExistError

        user.ensure_not_already_active()

        await self.user_gateway.change_active_status(user_id=user_id, is_active=True)
        await self.committer.commit()
