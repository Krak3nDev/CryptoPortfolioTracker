from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional

from cryptoapp.infrastructure.database.models.transactions import TransactionType


@dataclass
class UserDTO:
    id: int
    username: str
    email: Optional[str]
    password: str
    is_active: bool


@dataclass
class TransactionDTO:
    user_id: int
    quantity: Decimal
    price_per_unit: Decimal
    t_type: TransactionType
    transaction_date: datetime


@dataclass
class CreateUserDTO:
    username: str
    full_name: str
    email: str
    password: str
