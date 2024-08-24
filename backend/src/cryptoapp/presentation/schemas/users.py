from pydantic import BaseModel, EmailStr

from cryptoapp.infrastructure.dto.user import UserLoginDTO, CreateUserDTO


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
