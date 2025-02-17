from fastapi import FastAPI

from cryptoapp.main.init_routers import init_routers
from cryptoapp.main.log import setup_logging


def create_app() -> FastAPI:
    app = FastAPI()
    init_routers(app)
    setup_logging()
    return app
