from typing import Any

from cryptoapp.application.common.interactor import Interactor
from cryptoapp.application.dto.user import BasicUserDTO
from cryptoapp.application.interfaces.identifier import UserIdentifier
from cryptoapp.application.interfaces.repositories.user import UserGateway


class GetUserInformationInteractor(Interactor[Any, BasicUserDTO]):
    def __init__(self, identifier: UserIdentifier, user_repo: UserGateway):
        self.identifier = identifier
        self.user_repo = user_repo

    async def __call__(self, data: dict[str, str | int]) -> BasicUserDTO:
        user_id = self.identifier.get_user_id(data)
        user = await self.user_repo.get_user_by_id(user_id)

        user.ensure_is_active()

        return BasicUserDTO(user_id=user.id, username=user.username)
