from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Integer,
    String,
    Table,
    UniqueConstraint,
    false,
    text,
)
from sqlalchemy.orm import composite

from cryptoapp.application.common.validators import EMAIL_LENGTH
from cryptoapp.application.user.register_user import USERNAME_LENGTH
from cryptoapp.domain.entities.user.user import User, UserId
from cryptoapp.infrastructure.persistence.tables.base import mapper_registry

users_table = Table(
    "users",
    mapper_registry.metadata,
    Column("user_id", Integer, primary_key=True, autoincrement=True),
    Column("email", String(length=EMAIL_LENGTH), nullable=False),
    Column("username", String(length=USERNAME_LENGTH), nullable=False),
    Column("hashed_password", String(100), nullable=False),
    Column("is_active", Boolean, server_default=false()),
    Column(
        "created_at",
        DateTime(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    ),
    UniqueConstraint("email", name="uq_users_email"),
    UniqueConstraint("username", name="uq_users_username"),
)

mapper_registry.map_imperatively(
    User,
    users_table,
    properties={
        "_identity": composite(UserId, users_table.c.user_id),
        "_email": users_table.c.email,
        "_username": users_table.c.username,
        "_hashed_password": users_table.c.hashed_password,
        "_is_active": users_table.c.is_active,
    },
    exclude_properties=["created_at"],
)
