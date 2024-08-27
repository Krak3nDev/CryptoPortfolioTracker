from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, EmailStr

from cryptoapp.infrastructure.database.models.transactions import TransactionType
from cryptoapp.infrastructure.dto.data import UserLoginDTO, CreateUserDTO, TransactionDTO


class UserLogin(BaseModel):
    username: str
    password: str

    def to_dto(self) -> UserLoginDTO:
        return UserLoginDTO(
            username=self.username,
            password=self.password,
        )


class CreateUser(BaseModel):
    username: str
    full_name: str
    email: EmailStr
    password: str

    def to_dto(self) -> CreateUserDTO:
        return CreateUserDTO(
            username=self.username,
            full_name=self.full_name,
            email=self.email,
            password=self.password,
        )


class Transaction(BaseModel):
    user_id: int
    quantity: Decimal
    price_per_unit: Decimal
    transaction_type: TransactionType
    transaction_date: datetime

    def to_dto(self) -> TransactionDTO:
        return TransactionDTO(
            user_id=self.user_id,
            quantity=self.quantity,
            price_per_unit=self.price_per_unit,
            transaction_type=self.transaction_type,
            transaction_date=self.transaction_date
        )
