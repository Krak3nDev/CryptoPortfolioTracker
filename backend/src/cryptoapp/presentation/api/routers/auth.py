from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter
from pydantic import BaseModel, EmailStr
from starlette.requests import Request
from starlette.responses import Response

from cryptoapp.application.user.login import LoginInteractor, LoginRequestDTO
from cryptoapp.application.user.register_user import CreateUserDTO, RegisterInteractor
from cryptoapp.infrastructure.services.auth import Auther, LoginAuthDTO
from cryptoapp.infrastructure.services.session_manager import FastAPISessionManager

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    route_class=DishkaRoute,
)


@auth_router.post("/register")
async def register(
    data: CreateUserDTO,
    interactor: FromDishka[RegisterInteractor],
) -> dict[str, str]:
    await interactor(data=data)
    return {"message": "Registration was successful. Please check your email."}



@auth_router.post("/login")
async def login(
    data: LoginAuthDTO,
    response: Response,
    auther: FromDishka[Auther],
    session_manager: FromDishka[FastAPISessionManager],
    interactor: FromDishka[LoginInteractor],
) -> dict[str, str]:
    user_id = await auther.authenticate(
        data=data,
    )
    await interactor(data=LoginRequestDTO(data.username))
    await session_manager.init_session(user_id=user_id, response=response)
    return {"message": "You have successfully logged in."}


@auth_router.post("/logout")
async def logout(
    request: Request,
    response: Response,
    session_manager: FromDishka[FastAPISessionManager],
) -> dict[str, str]:
    await session_manager.invalidate_session(request=request, response=response)
    return {"message": "You have been logged out successfully."}
