from cryptoapp.domain.entities.user import User
from cryptoapp.infrastructure.dto.data import UserDTO


def convert_entity_to_dto(user: User) -> UserDTO:
    return UserDTO(
        id=None,
        username=user.username,
        email=user.email,
        password=None,
        is_active=user.is_active,
    )
