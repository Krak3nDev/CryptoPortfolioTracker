from typing import Annotated

from dishka import FromComponent, FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from cryptoapp.application.common.id_provider import IdProvider
from cryptoapp.application.user.activation import ActivateUserProfileInteractor
from cryptoapp.infrastructure.persistence.readers.user import (
    UserCredentials,
    UserReader,
)
from cryptoapp.infrastructure.services.session_id_provider import HTTPIdentityProvider

user_router = APIRouter(
    prefix="/users",
    tags=["users"],
    route_class=DishkaRoute,
)


@user_router.get("/confirm/{token}")
async def activate_user(
    interactor: Annotated[
        ActivateUserProfileInteractor, FromComponent("additional")
    ],
) -> dict[str, str]:
    await interactor()
    return {"message": "Activation was successful"}


@user_router.get("/me", response_model=UserCredentials)
async def get_current_user_credentials(
    identity_provider: FromDishka[IdProvider],
    reader: FromDishka[UserReader],
):
    user_id = await identity_provider.get_current_user_id()
    return await reader.get_credentials(user_id)
