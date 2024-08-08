from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

import jwt
from fastapi import HTTPException
from fastapi.security.utils import get_authorization_scheme_param
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED

from cryptoapp.application.dto.user import UserAuthDTO


def get_token_info(request: Request) -> str:
    authorization = request.headers.get("Authorization")
    scheme, param = get_authorization_scheme_param(authorization)
    if not authorization or scheme.lower() != "bearer":
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return param


class JWTService:
    TOKEN_TYPE_FIELD = "type"
    ACCESS_TOKEN_TYPE = "access"

    def __init__(
        self,
        private_key: str,
        public_key: str,
        algorithm: str,
        access_token_expire_minutes: int,
    ):
        self.private_key = private_key
        self.public_key = public_key
        self.algorithm = algorithm
        self.access_token_expire_minutes = access_token_expire_minutes

    def encode_jwt(
        self,
        payload: dict[str, Any],
        expire_minutes: Optional[int] = None,
        expire_timedelta: Optional[timedelta] = None,
    ) -> str:
        to_encode = payload.copy()
        now = datetime.now(timezone.utc)
        if expire_timedelta:
            expire = now + expire_timedelta
        else:
            expire = now + timedelta(
                minutes=expire_minutes
                if expire_minutes is not None
                else self.access_token_expire_minutes
            )
        to_encode.update(
            exp=expire,
            iat=now,
        )
        encoded = jwt.encode(
            to_encode,
            self.private_key,
            algorithm=self.algorithm,
        )
        return encoded

    def decode_jwt(self, token: str) -> Dict[str, int | str]:
        return jwt.decode(jwt=token, key=self.public_key, algorithms=[self.algorithm])  # type: ignore

    def create_jwt(
        self,
        token_type: str,
        token_data: Dict[str, str | str],
        expire_minutes: Optional[int] = None,
        expire_timedelta: Optional[timedelta] = None,
    ) -> str:
        jwt_payload = {self.TOKEN_TYPE_FIELD: token_type}
        jwt_payload.update(token_data)
        return self.encode_jwt(
            payload=jwt_payload,
            expire_minutes=expire_minutes,
            expire_timedelta=expire_timedelta,
        )

    def create_access_token(
        self, user: UserAuthDTO, expire_timedelta: Optional[timedelta] = None
    ) -> str:
        jwt_payload = {
            "sub": user.id,
            "username": user.username,
        }
        return self.create_jwt(
            token_type=self.ACCESS_TOKEN_TYPE,
            token_data=jwt_payload,
            expire_minutes=self.access_token_expire_minutes,
            expire_timedelta=expire_timedelta,
        )
