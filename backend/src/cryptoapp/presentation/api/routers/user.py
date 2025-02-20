import logging

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Query
from fastapi.responses import ORJSONResponse
from pydantic import BaseModel, EmailStr

from cryptoapp.application.user.activation import ActivateUserProfileInteractor
from cryptoapp.application.user.register_user import CreateUserDTO, RegisterInteractor

user_router = APIRouter(
    prefix="/users",
    tags=["users"],
    default_response_class=ORJSONResponse,
    route_class=DishkaRoute,
)


class CreateUserSchema(BaseModel):
    email: EmailStr
    username: str
    password: str

    def to_dto(self) -> CreateUserDTO:
        return CreateUserDTO(
            username=self.username, email=str(self.email), password=self.password
        )


@user_router.post("/")
async def register(
    data: CreateUserSchema,
    interactor: FromDishka[RegisterInteractor],
) -> ORJSONResponse:
    await interactor(data=data.to_dto())
    return ORJSONResponse(
        content={
            "message": "Registration was successful. Please check your email to confirm your account."
        },
        status_code=201,
    )


@user_router.get("/confirm")
async def activate_user(
    interactor: FromDishka[ActivateUserProfileInteractor],
    token: str = Query(...),
) -> ORJSONResponse:
    await interactor()
    return ORJSONResponse(
        content={"message": "Activation was successful"}, status_code=200
    )
