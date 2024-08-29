from cryptoapp.application.common.interactor import Interactor
from cryptoapp.domain.entities.user import User
from cryptoapp.domain.entities.user_id import UserId
from cryptoapp.infrastructure.dto.data import UserDTO


class LoginInteractor(Interactor[UserDTO, None]):
    def __call__(self, data: UserDTO) -> None:  # type: ignore
        user = User(
            id=UserId(data.id), username=data.username, is_active=data.is_active
        )
        user.ensure_is_active()
