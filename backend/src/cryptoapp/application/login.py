from cryptoapp.application.common.interactor import Interactor
from cryptoapp.application.dto.user import UserAccessDTO, UserLoginDTO
from cryptoapp.application.interfaces.authenticator import IAuthenticator
from cryptoapp.domain.entities.user import User


class LoginInteractor(Interactor[UserLoginDTO, UserAccessDTO]):
    def __init__(self, auth: IAuthenticator):
        self.authenticator = auth

    async def __call__(self, login_user: UserLoginDTO) -> User:
        authenticated_user = await self.authenticator.authenticate(
            login_user=login_user
        )
        return authenticated_user
