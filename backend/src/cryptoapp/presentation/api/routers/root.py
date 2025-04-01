from fastapi import APIRouter

from cryptoapp.presentation.api.routers.auth import auth_router
from cryptoapp.presentation.api.routers.portfolio import portfolio_router
from cryptoapp.presentation.api.routers.user import user_router

root_router = APIRouter()


root_router.include_router(user_router)
root_router.include_router(auth_router)
root_router.include_router(portfolio_router)


@root_router.get("/health")
async def root() -> dict[str, str]:
    return {"message": "success"}
