from datetime import timedelta

from cryptoapp.application.interfaces.generator import ActivationGenerator
from cryptoapp.infrastructure.services.jwt_service import JWTService
from cryptoapp.utils.constants import DOMAIN


class UrlGenerator(ActivationGenerator):
    def __init__(self, jwt_service: JWTService):
        self.jwt_service = jwt_service

    def generate(self, user_id: int) -> str:
        token_data = {"sub": user_id}
        token = self.jwt_service.create_jwt(
            token_type="activation",
            token_data=token_data,
            expire_timedelta=timedelta(hours=24),
        )
        return f"{DOMAIN}/jwt/confirm?token={token}"
