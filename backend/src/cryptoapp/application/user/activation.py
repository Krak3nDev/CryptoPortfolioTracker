from cryptoapp.application.common.id_provider import IdProvider
from cryptoapp.application.common.transaction_manager import TransactionManager
from cryptoapp.domain.entities.user.gateway import UserGateway


class ActivateUserProfileInteractor:
    def __init__(
        self,
        identity_provider: IdProvider,
        transaction_manager: TransactionManager,
        user_gateway: UserGateway,
    ):
        self.identity_provider = identity_provider
        self.transaction_manager = transaction_manager
        self.user_gateway = user_gateway

    async def __call__(self) -> None:
        user = await self.identity_provider.get_user()

        user.activate()

        await self.transaction_manager.commit()
