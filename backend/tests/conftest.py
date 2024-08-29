import pytest

from cryptoapp.config import load_config
from cryptoapp.infrastructure.database.setup import create_engine, create_session_pool

config = load_config()


@pytest.fixture(scope="session")
async def db_engine():
    engine = create_engine(config.db)
    yield engine
    await engine.dispose()


@pytest.fixture(scope="session")
async def session_pool(db_engine):
    return create_session_pool(db_engine)


@pytest.fixture(scope="function")
async def get_database_session(session_pool):
    async with session_pool() as session:
        yield session
        await session.rollback()
