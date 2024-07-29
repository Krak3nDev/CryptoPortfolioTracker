from fastapi import FastAPI
from jwt import ExpiredSignatureError

import cryptoapp.application.common.exceptions as exc
import cryptoapp.infrastructure.exceptions as infra_exc
import cryptoapp.domain.exceptions as domain_exc

from cryptoapp.presentation.routers.exc_handler import (
    already_activated_error_handler,
    authentication_error_handler,
    invalid_token_type_error_handler,
    token_expired_error_handler,
    user_already_exists_error_handler,
    user_not_active_error_handler,
)
from cryptoapp.presentation.routers.root import root_router


def init_routers(cryptoapp: FastAPI) -> None:
    cryptoapp.include_router(root_router)


def register_exception_handlers(cryptoapp: FastAPI) -> None:
    cryptoapp.add_exception_handler(
        exc.UserAlreadyExistsError, user_already_exists_error_handler
    )
    cryptoapp.add_exception_handler(domain_exc.UserNotActiveError, user_not_active_error_handler)
    cryptoapp.add_exception_handler(
        infra_exc.AuthenticationError, authentication_error_handler
    )
    cryptoapp.add_exception_handler(exc.InvalidTokenType, invalid_token_type_error_handler)
    cryptoapp.add_exception_handler(ExpiredSignatureError, token_expired_error_handler)
    cryptoapp.add_exception_handler(
        domain_exc.AlreadyActivatedException, already_activated_error_handler
    )
