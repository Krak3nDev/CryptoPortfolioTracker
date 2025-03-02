from contextlib import asynccontextmanager
from typing import AsyncContextManager, AsyncIterator, Callable

from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from taskiq_aio_pika import AioPikaBroker

from cryptoapp.main.config import load_config
from cryptoapp.main.di.setup import setup_ioc_container
from cryptoapp.main.init_routers import init_routers
from cryptoapp.main.log import setup_logging
from cryptoapp.main.taskiq_entry.broker import create_broker
from cryptoapp.main.web_errors import register_exception_handlers


def broker_startup_lifespan(
    broker: AioPikaBroker,
) -> Callable[[FastAPI], AsyncContextManager[None]]:
    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        if not broker.is_worker_process:
            await broker.startup()
        yield
        await broker.shutdown()
        await app.state.dishka_container.close()

    return lifespan


def create_app() -> FastAPI:
    config = load_config()

    broker = create_broker(config)

    app = FastAPI(
        lifespan=broker_startup_lifespan(broker), default_response_class=ORJSONResponse
    )

    init_routers(app)
    register_exception_handlers(app)
    setup_logging()

    container = setup_ioc_container(config=config, broker=broker)
    setup_dishka(container=container, app=app)

    return app
