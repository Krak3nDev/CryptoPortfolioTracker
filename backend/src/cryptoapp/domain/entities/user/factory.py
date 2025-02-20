from cryptoapp.domain.entities.user.gateway import UserGateway
from cryptoapp.domain.entities.user.hasher import PasswordHasher
from cryptoapp.domain.entities.user.user import User
from cryptoapp.domain.entities.user.user_id import UserId
from cryptoapp.domain.exceptions import UserAlreadyExistsError
from cryptoapp.domain.value_objects.email import Email


class UserFactory:
    def __init__(self, user_gateway: UserGateway, hasher: PasswordHasher) -> None:
        self.user_gateway = user_gateway
        self.hasher = hasher

    async def create(
        self, username: str, email: str, password: str, user_id: int | None
    ) -> User:
        email_vo = Email(email)

        if await self.user_gateway.is_username_or_email_taken(
            username=username, email=email_vo.value
        ):
            raise UserAlreadyExistsError(username=username, email=email_vo.value)

        hashed_password = self.hasher.hash(password)

        user = User(
            _identity=UserId(value=user_id),
            _email=email_vo,
            _hashed_password=hashed_password,
            _username=username,
            _is_active=False,
        )

        self.user_gateway.add(user=user)

        return user
