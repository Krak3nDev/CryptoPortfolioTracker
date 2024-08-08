from cryptoapp.application.common.interactor import Interactor
from cryptoapp.application.dto.user import UserLoginDTO, UserDTO
from cryptoapp.application.interfaces.authenticator import Authenticator
from cryptoapp.infrastructure.dto.converters import convert_entity_to_dto


class LoginInteractor(Interactor[UserLoginDTO, UserDTO]):
    def __init__(self, auth: Authenticator):
        self.authenticator = auth

    async def __call__(self, login_user: UserLoginDTO) -> UserDTO:
        authenticated_user = await self.authenticator.authenticate(
            login_user=login_user
        )
        return convert_entity_to_dto(authenticated_user)
