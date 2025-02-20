from fastapi import APIRouter

from cryptoapp.presentation.api.routers.user import user_router

root_router = APIRouter()


root_router.include_router(user_router)


@root_router.get("/")
async def root() -> dict[str, str]:
    return {"message": "success"}
