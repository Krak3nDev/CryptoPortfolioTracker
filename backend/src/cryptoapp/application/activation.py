from typing import Dict

from cryptoapp.application.common.exceptions import (
    InvalidTokenType,
)
from cryptoapp.application.common.interactor import Interactor
from cryptoapp.application.interfaces.committer import Committer
from cryptoapp.application.interfaces.identifier import UserIdentifier
from cryptoapp.application.interfaces.repositories.user import UserGateway


class ActivationInteractor(Interactor[str, None]):
    def __init__(self, user_gateway: UserGateway, committer: Committer, identifier: UserIdentifier):
        self.user_gateway = user_gateway
        self.committer = committer
        self.identifier = identifier

    async def __call__(self, data: Dict[str, str | int]) -> None:
        if data.get("type") != "activation":
            raise InvalidTokenType()

        user_id = self.identifier.get_user_id(data=data)

        user = await self.user_gateway.get_by_id(user_id)

        user.ensure_not_already_active()

        await self.user_gateway.change_active_status(user_id=user_id, is_active=True)
        await self.committer.commit()
