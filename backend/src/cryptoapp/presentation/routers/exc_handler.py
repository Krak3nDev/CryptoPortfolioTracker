from fastapi import Request
from starlette.responses import JSONResponse


async def user_already_exists_error_handler(
    request: Request, exception: Exception
) -> JSONResponse:
    return JSONResponse(status_code=409, content={"detail": "User already exists"})


async def user_not_active_error_handler(
    request: Request, exception: Exception
) -> JSONResponse:
    return JSONResponse(status_code=401, content={"detail": "User is not active"})


async def authentication_error_handler(
    request: Request, exception: Exception
) -> JSONResponse:
    return JSONResponse(
        status_code=401, content={"detail": "Invalid username or password"}
    )


async def invalid_token_type_error_handler(
    request: Request, exception: Exception
) -> JSONResponse:
    return JSONResponse(status_code=400, content={"detail": "Invalid token type"})


async def token_expired_error_handler(
    request: Request, exception: Exception
) -> JSONResponse:
    return JSONResponse(status_code=401, content={"detail": "Token has expired"})


async def already_activated_error_handler(
    request: Request, exception: Exception
) -> JSONResponse:
    return JSONResponse(
        status_code=409,
        content={"detail": "This account has already been activated."},
    )
