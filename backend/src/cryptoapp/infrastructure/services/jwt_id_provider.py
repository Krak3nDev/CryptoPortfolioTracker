from cryptoapp.application.interfaces.id_provider import IdProvider
from cryptoapp.domain.entities.user_id import UserId
from cryptoapp.infrastructure.dto.data import TokenPayloadDTO


class TokenIdProvider(IdProvider):
    def __init__(
        self,
        token: TokenPayloadDTO,
    ) -> None:
        self.token = token

    def get_current_user_id(self) -> UserId:
        return UserId(self.token.sub)
