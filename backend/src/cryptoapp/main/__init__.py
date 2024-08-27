__all__ = [
    "create_app",
    "init_routers",
]

from .router_registration import init_routers
from .web import create_app
