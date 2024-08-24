from cryptoapp.application.interfaces.authenticator import Authenticator
from cryptoapp.application.interfaces.gateways.user import UserGateway
from cryptoapp.application.interfaces.hasher import IPasswordHasher
from cryptoapp.infrastructure.dto.user import UserDTO, UserLoginDTO
from cryptoapp.infrastructure.exceptions import AuthenticationError


class AuthService(Authenticator):
    def __init__(self, user_gateway: UserGateway, hasher: IPasswordHasher):
        self.user_gateway = user_gateway
        self.hasher = hasher

    async def authenticate(self, login_user: UserLoginDTO) -> UserDTO:
        user = await self.user_gateway.get_with_password(login_user.username)

        if not user or not self.hasher.verify(
            password=login_user.password,
            hashed_password=user.password if user.password else ""):
            raise AuthenticationError("Invalid username or password")

        return user
