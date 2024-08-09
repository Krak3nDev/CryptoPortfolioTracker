from dataclasses import dataclass
from typing import Optional


@dataclass
class TokenInfo:
    access_token: str
    token_type: str = "Bearer"


@dataclass
class TokenPayloadDTO:
    sub: int
    username: str
    exp: Optional[int] = None
    iat: Optional[int] = None
    type: Optional[str] = None
