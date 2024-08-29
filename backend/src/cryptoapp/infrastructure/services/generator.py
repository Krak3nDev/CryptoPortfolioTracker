from datetime import timedelta

from cryptoapp.application.interfaces.generator import ActivationGenerator
from cryptoapp.config import DomainConfig
from cryptoapp.infrastructure.services.jwt_service import JwtTokenProcessor, TokenType


class UrlGenerator(ActivationGenerator):
    def __init__(self, jwt_service: JwtTokenProcessor, domain_config: DomainConfig):
        self.jwt_service = jwt_service
        self.config = domain_config

    def generate(self, user_id: int) -> str:
        token_data = {"sub": str(user_id)}
        token = self.jwt_service.create_jwt(
            token_type=TokenType.ACTIVATION,
            token_data=token_data,
            expire_timedelta=timedelta(hours=24),
        )
        return f"{self.config.domain}/jwt/confirm?token={token}"
