from cryptoapp.application.dto.user import UserDTO
from cryptoapp.domain.entities.user import User


def convert_entity_to_dto(user: User) -> UserDTO:
    return UserDTO(
        id=user.id,
        username=user.username,
        email=user.email,
        password=None,
        is_active=user.is_active
    )
