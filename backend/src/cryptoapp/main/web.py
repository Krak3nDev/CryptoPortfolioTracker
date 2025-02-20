from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

from cryptoapp.main.config import load_config
from cryptoapp.main.di.setup import setup_ioc_container
from cryptoapp.main.init_routers import init_routers
from cryptoapp.main.log import setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    yield
    await app.state.dishka_container.close()


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    config = load_config()

    init_routers(app)
    setup_logging()
    setup_ioc_container(config=config, app=app)
    return app
