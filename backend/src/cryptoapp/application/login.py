from cryptoapp.application.common.interactor import Interactor
from cryptoapp.application.interfaces.authenticator import Authenticator
from cryptoapp.infrastructure.dto.user import UserLoginDTO, UserDTO


class LoginInteractor(Interactor[UserLoginDTO, UserDTO]):
    def __init__(self, auth: Authenticator):
        self.authenticator = auth

    async def __call__(self, login_user: UserLoginDTO) -> UserDTO:
        authenticated_user = await self.authenticator.authenticate(
            login_user=login_user
        )
        return authenticated_user
