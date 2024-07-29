from fastapi import APIRouter

from .jwt_auth import auth_router
from .market_data import market_router

root_router = APIRouter()

root_router.include_router(
    market_router,
)
root_router.include_router(
    auth_router,
)
