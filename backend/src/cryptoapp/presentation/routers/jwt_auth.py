from typing import Dict

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from cryptoapp.application.activation import ActivationInteractor
from cryptoapp.application.login import LoginInteractor
from cryptoapp.application.register_user import RegisterInteractor
from cryptoapp.infrastructure.dto.data import TokenInfo, TokenPayloadDTO
from cryptoapp.infrastructure.services.auth import AuthService
from cryptoapp.infrastructure.services.confirmation_token import check_token_type
from cryptoapp.presentation.schemas.common import CreateUser, UserLogin

auth_router = APIRouter(prefix="/jwt", route_class=DishkaRoute, tags=["auth"])


@auth_router.post("/signup")
async def signup(
    register: FromDishka[RegisterInteractor],
    user: CreateUser,
) -> Dict[str, str]:
    await register(user.to_dto())
    return {"message": "User successfully registered"}


@auth_router.post("/login", response_model=TokenInfo)
async def login(
    auth_service: FromDishka[AuthService],
    login_interactor: FromDishka[LoginInteractor],
    user: UserLogin,
) -> TokenInfo:
    token, user_dto = await auth_service.authenticate(user.to_dto())
    login_interactor(user_dto)
    return TokenInfo(access_token=token, token_type="Bearer")


@auth_router.get("/confirm")
async def activation(
    token: FromDishka[TokenPayloadDTO],
    activation_interactor: FromDishka[ActivationInteractor],
) -> Dict[str, str]:
    check_token_type(token)
    await activation_interactor()
    return {"message": "Email successfully confirmed."}


@auth_router.post("/logout", dependencies=[Depends(HTTPBearer())])
async def logout() -> Dict[str, str]:
    return {"message": "Successfully logged out"}
