from typing import Annotated

from dishka import FromComponent
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from cryptoapp.application.user.activation import ActivateUserProfileInteractor

user_router = APIRouter(
    prefix="/users",
    tags=["users"],
    route_class=DishkaRoute,
)


@user_router.get("/confirm/{token}")
async def activate_user(
    interactor: Annotated[ActivateUserProfileInteractor, FromComponent("additional")],
) -> dict[str, str]:
    await interactor()
    return {"message": "Activation was successful"}
