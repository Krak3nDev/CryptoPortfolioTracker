from dataclasses import dataclass


@dataclass
class TokenInfo:
    access_token: str
    token_type: str = "Bearer"
