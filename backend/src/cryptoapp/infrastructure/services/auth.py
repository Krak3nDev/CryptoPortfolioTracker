from cryptoapp.application.dto.user import UserAccessDTO, UserLoginDTO
from cryptoapp.application.interfaces.authenticator import IAuthenticator
from cryptoapp.application.interfaces.hasher import IPasswordHasher
from cryptoapp.application.interfaces.repositories.user import UserRepo
from cryptoapp.domain.entities.user import User
from cryptoapp.domain.entities.user_id import UserId
from cryptoapp.infrastructure.exceptions import AuthenticationError


class AuthService(IAuthenticator):
    def __init__(self, repo: UserRepo, hasher: IPasswordHasher):
        self.repo = repo
        self.hasher = hasher

    async def authenticate(self, login_user: UserLoginDTO) -> User:
        user = await self.repo.get_user_by_username(login_user.username)

        if not user or not self.hasher.verify(login_user.password, user.password):
            raise AuthenticationError("Invalid username or password")

        return User(
            id=UserId(user.id),
            username=login_user.username,
            is_active=user.is_active,
            email=None,
            password=None
        )
