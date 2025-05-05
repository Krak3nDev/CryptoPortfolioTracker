from contextlib import asynccontextmanager
from typing import AsyncContextManager, AsyncIterator, Callable

from dishka import AsyncContainer
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from taskiq import AsyncBroker

from cryptoapp.main.config import load_config
from cryptoapp.main.di.setup import setup_ioc_container
from cryptoapp.main.init_routers import init_routers
from cryptoapp.main.log import setup_logging
from cryptoapp.main.taskiq_entry.broker import create_broker
from cryptoapp.main.web_errors import register_exception_handlers


def broker_startup_lifespan(
    broker: AsyncBroker,
) -> Callable[[FastAPI], AsyncContextManager[None]]:
    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        if not broker.is_worker_process:
            await broker.startup()
        yield
        await broker.shutdown()
        await app.state.dishka_container.close()

    return lifespan


def create_app(broker: AsyncBroker, container: AsyncContainer) -> FastAPI:
    app = FastAPI(
        lifespan=broker_startup_lifespan(broker),
        default_response_class=ORJSONResponse,
    )

    origins_dev = [
        "http://localhost",
        "http://127.0.0.1",
        "http://localhost:4200",
        "http://127.0.0.1:4200",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins_dev,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    init_routers(app)
    register_exception_handlers(app)
    setup_logging()

    setup_dishka(container=container, app=app)

    return app

def main() -> FastAPI:
    config = load_config()
    broker = create_broker(config)
    container = setup_ioc_container(config=config, broker=broker)
    app = create_app(broker=broker, container=container)
    return app
