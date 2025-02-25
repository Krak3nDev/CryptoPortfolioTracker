from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from starlette.requests import Request

from cryptoapp.domain.exceptions import DomainError


async def domain_error_handler(
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


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(DomainError, domain_error_handler)
