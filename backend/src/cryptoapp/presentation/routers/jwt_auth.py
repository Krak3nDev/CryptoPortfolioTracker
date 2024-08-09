from typing import Dict

from cryptoapp.application.dto.user import BasicUserDTO
from cryptoapp.infrastructure.dto.common import TokenInfo
from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from starlette.requests import Request

from cryptoapp.application.activation import ActivationInteractor
from cryptoapp.application.get_user_info import GetUserInformationInteractor
from cryptoapp.application.login import LoginInteractor
from cryptoapp.application.register_user import RegisterInteractor
from cryptoapp.infrastructure.services.jwt_service import JWTService, get_token_info
from cryptoapp.presentation.schemas.users import CreateUser, UserLogin

auth_router = APIRouter(prefix="/jwt", route_class=DishkaRoute, tags=["auth"])
security = Depends(HTTPBearer())


@auth_router.post("/signup")
async def signup(
    user_service: FromDishka[RegisterInteractor],
    user: CreateUser,
) -> Dict[str, str]:
    await user_service(user.to_dto())
    return {"message": "User successfully registered"}


@auth_router.post("/login", response_model=TokenInfo)
async def login(
    jwt_service: FromDishka[JWTService],
    login_interactor: FromDishka[LoginInteractor],
    user: UserLogin,
) -> TokenInfo:
    authenticated_user = await login_interactor(login_user=user.to_dto())
    token = jwt_service.create_access_token(
        user=authenticated_user,
    )
    return TokenInfo(access_token=token, token_type="Bearer")


@auth_router.get("/users/me/", response_model=BasicUserDTO, dependencies=[security])
async def me(
    request: Request,
    jwt_service: FromDishka[JWTService],
    user_info: FromDishka[GetUserInformationInteractor],
) -> BasicUserDTO:
    token = get_token_info(request)
    token_info = jwt_service.decode_jwt(token)
    user = await user_info(token_info)
    return user


@auth_router.get("/confirm")
async def activation(
    token: str,
    jwt_service: FromDishka[JWTService],
    activation_interactor: FromDishka[ActivationInteractor],
) -> Dict[str, str]:
    token_payload = jwt_service.decode_jwt(token)
    await activation_interactor(token_payload)
    return {"message": "Email successfully confirmed."}


@auth_router.post("/logout")
async def logout() -> Dict[str, str]:
    return {"message": "Successfully logged out"}
