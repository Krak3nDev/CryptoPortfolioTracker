from cryptoapp.application.interfaces.gateways.user import UserGateway
from cryptoapp.application.interfaces.hasher import IPasswordHasher
from cryptoapp.infrastructure.dto.data import UserLoginDTO, UserDTO
from cryptoapp.infrastructure.exceptions import AuthenticationError
from cryptoapp.infrastructure.services.jwt_service import JwtTokenProcessor


class AuthService:
    def __init__(
        self, user_gateway: UserGateway, hasher: IPasswordHasher, jwt: JwtTokenProcessor
    ) -> None:
        self.user_gateway = user_gateway
        self.hasher = hasher
        self.jwt = jwt

    async def _check_user(self, login_user: UserLoginDTO) -> UserDTO:
        user = await self.user_gateway.get_with_password(login_user.username)

        if not user or not self.hasher.verify(
            password=login_user.password, hashed_password=user.password
        ):
            raise AuthenticationError

        return user

    async def authenticate(self, login_user: UserLoginDTO) -> tuple[str, UserDTO]:
        user = await self._check_user(login_user)
        token = self.jwt.create_access_token(user=user)
        return token, user
