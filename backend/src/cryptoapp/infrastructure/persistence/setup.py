from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from cryptoapp.main.config import DbConfig


def create_engine(db: DbConfig) -> AsyncEngine:
    engine = create_async_engine(
        db.url,
        query_cache_size=1200,
        pool_size=20,
        max_overflow=200,
        future=True,
        echo=False,
    )
    return engine


def create_session_pool(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    session_pool = async_sessionmaker(bind=engine, expire_on_commit=False)
    return session_pool
