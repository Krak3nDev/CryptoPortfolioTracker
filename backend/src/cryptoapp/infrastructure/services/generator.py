import uuid

from redis.asyncio import Redis

from cryptoapp.application.interfaces.generator import ActivationGenerator
from cryptoapp.main.config import UrlConfig


class UrlGenerator(ActivationGenerator):
    def __init__(self, redis: Redis, url_config: UrlConfig):
        self.config = url_config
        self.redis = redis

    async def generate_url(self, user_id: int) -> str:
        activation_token = str(uuid.uuid4())
        ttl_hours = 1

        await self.redis.setex(
            name=activation_token, value=str(user_id), time=ttl_hours * 3600
        )

        return f"{self.config.base_url}/users/confirm/{activation_token}"
