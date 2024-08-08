from typing import Any

from cryptoapp.application.dto.user import UserDTO

from cryptoapp.application.common.exceptions import UserDoesNotExistError
from cryptoapp.application.common.interactor import Interactor
from cryptoapp.application.interfaces.identifier import UserIdentifier
from cryptoapp.application.interfaces.repositories.user import UserGateway
from cryptoapp.infrastructure.dto.converters import convert_entity_to_dto


class GetUserInformationInteractor(Interactor[Any, UserDTO]):
    def __init__(self, identifier: UserIdentifier, user_gateway: UserGateway):
        self.identifier = identifier
        self.user_gateway = user_gateway

    async def __call__(self, data: dict[str, str | int]) -> UserDTO:
        user_id = self.identifier.get_user_id(data)
        user = await self.user_gateway.get_by_id(user_id)

        if not user:
            raise UserDoesNotExistError()

        user.ensure_is_active()

        return convert_entity_to_dto(user)
