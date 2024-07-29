from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from cryptoapp.main.depedencies.main_provider import MainProvider
from cryptoapp.main.routers import init_routers, register_exception_handlers
from cryptoapp.utils.log import setup_logging


def init_dependencies(app: FastAPI) -> None:
    provider = MainProvider()
    container = make_async_container(provider)
    setup_dishka(container=container, app=app)


def create_app() -> FastAPI:
    app = FastAPI()
    init_dependencies(app)
    init_routers(app)
    register_exception_handlers(app)
    setup_logging()
    return app
