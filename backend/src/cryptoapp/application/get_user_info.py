from typing import Any

from cryptoapp.application.common.interactor import Interactor
from cryptoapp.application.dto.user import BasicUserDTO
from cryptoapp.application.interfaces.identifier import IUserIdentifier
from cryptoapp.application.interfaces.repositories.user import UserRepo


class GetUserInformationInteractor(Interactor[Any, BasicUserDTO]):
    def __init__(self, identifier: IUserIdentifier, user_repo: UserRepo):
        self.identifier = identifier
        self.user_repo = user_repo

    async def __call__(self, data: Any) -> BasicUserDTO:
        user_id = self.identifier.get_user_id(data)
        user = await self.user_repo.get_user_by_id(user_id)

        user.ensure_is_active()

        return BasicUserDTO(user_id=user.id, username=user.username)
