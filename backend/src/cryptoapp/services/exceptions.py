from fastapi import HTTPException
from starlette import status

unregistered_user_exc = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="user not registered",
)

unauthed_exc = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="invalid username or password",
)

unactive_exc = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="user inactive. Please verify your email.",
)
