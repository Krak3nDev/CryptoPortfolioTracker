from cryptoapp.application.interfaces.id_provider import IdProvider
from cryptoapp.domain.entities.user_id import UserId
from cryptoapp.infrastructure.services.jwt_service import JwtTokenProcessor


class TokenIdProvider(IdProvider):
    def __init__(
        self,
        token_processor: JwtTokenProcessor,
        token: str,
    ) -> None:
        self.token_processor = token_processor
        self.token = token

    def get_current_user_id(self) -> UserId:
        return self.token_processor.validate_user_id(self.token)
