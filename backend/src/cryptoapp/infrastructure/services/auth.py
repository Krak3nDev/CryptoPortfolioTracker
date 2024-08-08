from cryptoapp.application.dto.user import UserLoginDTO, UserAuthDTO
from cryptoapp.application.interfaces.authenticator import IAuthenticator
from cryptoapp.application.interfaces.hasher import IPasswordHasher
from cryptoapp.application.interfaces.repositories.user import UserGateway
from cryptoapp.infrastructure.exceptions import AuthenticationError


class AuthService(IAuthenticator):
    def __init__(self, user_gateway: UserGateway, hasher: IPasswordHasher):
        self.user_gateway = user_gateway
        self.hasher = hasher

    async def authenticate(self, login_user: UserLoginDTO) -> UserAuthDTO:
        user = await self.user_gateway.get_current_user_with_password(login_user.username)

        if not user or not self.hasher.verify(password=login_user.password,
                                              hashed_password=user.password):
            raise AuthenticationError("Invalid username or password")

        return user
