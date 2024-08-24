from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from cryptoapp.infrastructure.services.scheduler import start_scheduler
from cryptoapp.main.depedencies.ioc_container import container
from cryptoapp.main.routers import init_routers, register_exception_handlers
from cryptoapp.utils.log import setup_logging


def create_app() -> FastAPI:
    app = FastAPI()
    setup_dishka(container=container, app=app)
    init_routers(app)
    start_scheduler()
    register_exception_handlers(app)
    setup_logging()
    return app
