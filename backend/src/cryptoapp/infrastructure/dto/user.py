from dataclasses import dataclass
from typing import Optional


@dataclass
class UserDTO:
    id: int
    username: str
    email: str
    password: Optional[str]
    is_active: bool


@dataclass
class UserAuthDTO:
    id: int
    username: str
    email: str
    password: str
    is_active: bool


@dataclass
class UserAccessDTO:
    user_id: int
    username: str
    is_active: bool


@dataclass
class CreateUserDTO:
    username: str
    full_name: str
    email: str
    password: str


@dataclass
class AuthUserDTO:
    user_id: int
    hashed_password: str
    active: bool


@dataclass
class UserLoginDTO:
    username: str
    password: str


@dataclass
class TokenInfo:
    access_token: str
    token_type: str = "Bearer"
