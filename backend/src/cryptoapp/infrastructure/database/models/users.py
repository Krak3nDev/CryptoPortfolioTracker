from sqlalchemy import BIGINT, Boolean, String, false
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, TimestampMixin


class UserDB(Base, TimestampMixin):
    __tablename__ = "users"
    user_id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    full_name: Mapped[str] = mapped_column(String(255))
    username: Mapped[str] = mapped_column(String(255), unique=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    password_hash: Mapped[str] = mapped_column(String)
    is_active: Mapped[bool] = mapped_column(Boolean, server_default=false())
