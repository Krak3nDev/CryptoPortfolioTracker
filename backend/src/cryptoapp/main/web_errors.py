from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from starlette.requests import Request

from cryptoapp.application.exceptions import ApplicationError, UserIsNotRegistered
from cryptoapp.domain.exceptions import DomainError
from cryptoapp.infrastructure.exceptions import UnauthorizedError


async def business_logic_error_handler(
    request: Request, exception: Exception
) -> ORJSONResponse:
    return ORJSONResponse(status_code=409, content={"detail": str(exception)})


async def validation_error_handler(
    request: Request, exception: Exception
) -> ORJSONResponse:
    return ORJSONResponse(
        status_code=422,
        content={"detail": str(exception)},
    )


async def unauthorized_error_handler(
    request: Request, exception: Exception
) -> ORJSONResponse:
    return ORJSONResponse(
        status_code=401,
        content={"detail": str(exception)},
    )


async def user_not_registered_error_handler(
    request: Request, exception: Exception
) -> ORJSONResponse:
    return ORJSONResponse(
        status_code=404,
        content={"detail": str(exception)},
    )


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(DomainError, business_logic_error_handler)
    app.add_exception_handler(ApplicationError, business_logic_error_handler)
    app.add_exception_handler(UnauthorizedError, unauthorized_error_handler)
    app.add_exception_handler(UserIsNotRegistered, user_not_registered_error_handler)
