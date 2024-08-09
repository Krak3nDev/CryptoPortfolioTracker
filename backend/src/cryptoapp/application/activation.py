from cryptoapp.application.common.exceptions import (
    InvalidTokenType, UserDoesNotExistError,
)
from cryptoapp.application.common.interactor import Interactor
from cryptoapp.application.interfaces.committer import Committer
from cryptoapp.application.interfaces.repositories.user import UserGateway
from cryptoapp.infrastructure.dto.jwt import TokenPayloadDTO
from cryptoapp.infrastructure.services.jwt_service import TokenType


class ActivationInteractor(Interactor[TokenPayloadDTO, None]):
    def __init__(self, user_gateway: UserGateway, committer: Committer):
        self.user_gateway = user_gateway
        self.committer = committer

    async def __call__(self, data: TokenPayloadDTO) -> None:
        if TokenPayloadDTO.type != TokenType.ACTIVATION:
            raise InvalidTokenType()

        user = await self.user_gateway.get_by_id(data.sub)

        if not user:
            raise UserDoesNotExistError()

        user.ensure_not_already_active()

        await self.user_gateway.change_active_status(user_id=data.sub, is_active=True)
        await self.committer.commit()
