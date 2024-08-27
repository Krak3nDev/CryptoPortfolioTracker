from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional

from cryptoapp.infrastructure.database.models.transactions import TransactionType


@dataclass
class UserDTO:
    id: Optional[int]
    username: str
    email: Optional[str]
    password: str
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
class TransactionDTO:
    user_id: int
    quantity: Decimal
    price_per_unit: Decimal
    transaction_type: TransactionType
    transaction_date: datetime


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
