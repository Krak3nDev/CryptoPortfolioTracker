from dishka import FromDishka
from fastapi import APIRouter
from starlette.requests import Request

from cryptoapp.application.get_user_info import GetUserInformationInteractor
from cryptoapp.infrastructure.dto.data import UserDTO
from cryptoapp.infrastructure.services.jwt_service import (
    JwtTokenProcessor,
    get_token_info,
)
from . import security

user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.get("/me/", response_model=UserDTO, dependencies=[security])
async def get_me(
    request: Request,
    jwt_service: FromDishka[JwtTokenProcessor],
    user_info: FromDishka[GetUserInformationInteractor],
) -> UserDTO:
    token = get_token_info(request)
    token_info = jwt_service.decode_jwt(token)
    user = await user_info(token_info)
    return user
