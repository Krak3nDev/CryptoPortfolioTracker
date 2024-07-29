import cryptoapp.application.common.exceptions as exc
import cryptoapp.infrastructure.exceptions as infra_exc
import cryptoapp.domain.exceptions as domain_exc
from fastapi import Request
from jwt import ExpiredSignatureError
from starlette.responses import JSONResponse


async def user_already_exists_error_handler(
    request: Request, exception: exc.UserAlreadyExistsError
) -> JSONResponse:
    return JSONResponse(status_code=409, content={"detail": "User already exists"})


async def user_not_active_error_handler(
    request: Request, exception: domain_exc.UserNotActiveError
) -> JSONResponse:
    return JSONResponse(status_code=401, content={"detail": "User is not active"})


async def authentication_error_handler(
    request: Request, exception: infra_exc.AuthenticationError
) -> JSONResponse:
    return JSONResponse(
        status_code=401, content={"detail": "Invalid username or password"}
    )


async def invalid_token_type_error_handler(
    request: Request, exception: exc.InvalidTokenType
) -> JSONResponse:
    return JSONResponse(status_code=400, content={"detail": "Invalid token type"})


async def token_expired_error_handler(
    request: Request, exception: ExpiredSignatureError
) -> JSONResponse:
    return JSONResponse(status_code=401, content={"detail": "Token has expired"})


async def already_activated_error_handler(
    request: Request, exception: domain_exc.AlreadyActivatedException
) -> JSONResponse:
    return JSONResponse(
        status_code=409,
        content={"detail": "This account has already been activated."},
    )
