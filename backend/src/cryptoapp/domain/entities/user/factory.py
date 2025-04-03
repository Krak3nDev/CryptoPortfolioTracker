from cryptoapp.domain.entities.user.gateway import UserGateway
from cryptoapp.domain.entities.user.hasher import PasswordHasher
from cryptoapp.domain.entities.user.user import User
from cryptoapp.domain.exceptions import UserAlreadyExistsError


class UserFactory:
    def __init__(
        self, user_gateway: UserGateway, hasher: PasswordHasher
    ) -> None:
        self.user_gateway = user_gateway
        self.hasher = hasher

    async def create(
        self, username: str, email: str, password: str, user_id: int | None
    ) -> User:
        availability_info = (
            await self.user_gateway.get_username_email_availability(
                username, email
            )
        )

        if availability_info is not None:
            is_username_taken = availability_info["username"] == username
            is_email_taken = availability_info["email"] == email

            raise UserAlreadyExistsError(
                username=username if is_username_taken else None,
                email=email if is_email_taken else None,
            )

        hashed_password = self.hasher.hash(password)

        return User.create(
            user_id=user_id,
            email=email,
            hashed_password=hashed_password,
            username=username,
        )
