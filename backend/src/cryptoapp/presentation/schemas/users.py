from typing import Optional

from cryptoapp.application.dto.user import CreateUserDTO, UserLoginDTO
from pydantic import BaseModel, EmailStr


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


class UserPydantic(BaseModel):
    id: int
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
