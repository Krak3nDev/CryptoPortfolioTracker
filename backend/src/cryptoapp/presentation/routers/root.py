from fastapi import APIRouter

from .jwt_auth import auth_router

root_router = APIRouter()

# root_router.include_router(
#     portfolio_router,
# )
root_router.include_router(
    auth_router,
)
