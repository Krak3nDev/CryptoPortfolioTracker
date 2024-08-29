from cryptoapp.infrastructure.dto.data import TokenPayloadDTO
from cryptoapp.infrastructure.exceptions import InvalidTokenType
from cryptoapp.infrastructure.services.jwt_service import TokenType


def check_token_type(token: TokenPayloadDTO) -> None:
    if token.type != TokenType.ACTIVATION:
        raise InvalidTokenType
