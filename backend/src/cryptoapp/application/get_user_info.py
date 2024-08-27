from cryptoapp.application.common.exceptions import UserDoesNotExistError
from cryptoapp.application.common.interactor import Interactor
from cryptoapp.application.interfaces.gateways.user import UserGateway
from cryptoapp.infrastructure.dto.converters import convert_entity_to_dto
from cryptoapp.infrastructure.dto.data import UserDTO, TokenPayloadDTO


class GetUserInformationInteractor(Interactor[TokenPayloadDTO, UserDTO]):
    def __init__(self, user_gateway: UserGateway):
        self.user_gateway = user_gateway

    async def __call__(self, data: TokenPayloadDTO) -> UserDTO:
        user = await self.user_gateway.get_by_id(data.sub)

        if not user:
            raise UserDoesNotExistError()

        user.ensure_is_active()

        return convert_entity_to_dto(user)
