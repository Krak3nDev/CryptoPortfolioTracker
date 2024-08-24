from typing import AsyncIterator

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from cryptoapp.config import Config, load_config
from cryptoapp.infrastructure.database.setup import create_engine, create_session_pool
from cryptoapp.infrastructure.services.api.coin_market import CoinMarketApi
from cryptoapp.infrastructure.services.committer import SQLAlchemyCommitter


class CoreProvider(Provider):
    @provide(scope=Scope.APP)
    def get_config(self) -> Config:
        return load_config()

    @provide(scope=Scope.APP)
    def get_coin_market_api(self, config: Config) -> CoinMarketApi:
        return CoinMarketApi(
            api_key=config.coin_market.api_key, base_url=config.coin_market.base_url
        )

    @provide(scope=Scope.APP)
    def get_session_pool(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return create_session_pool(engine)

    @provide(scope=Scope.APP)
    def get_engine(self, config: Config) -> AsyncEngine:
        return create_engine(config.db)

    @provide(scope=Scope.REQUEST)
    async def get_uow(
        self, session_pool: async_sessionmaker[AsyncSession]
    ) -> AsyncIterator[SQLAlchemyCommitter]:
        async with session_pool() as session:
            yield SQLAlchemyCommitter(session)
