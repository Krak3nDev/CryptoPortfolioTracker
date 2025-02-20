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

from cryptoapp.domain.entities.user.user import User
from cryptoapp.domain.entities.user.user_id import UserId
from cryptoapp.domain.value_objects.email import Email
from cryptoapp.infrastructure.persistence.tables.base import mapper_registry

users_table = Table(
    "users",
    mapper_registry.metadata,
    Column("user_id", Integer, primary_key=True, autoincrement=True),
    Column("email", String(length=320), nullable=False),
    Column("username", String(length=50), nullable=False),
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
        "_email": composite(Email, users_table.c.email),
        "_username": users_table.c.username,
        "_hashed_password": users_table.c.hashed_password,
        "_is_active": users_table.c.is_active,
    },
    exclude_properties=["created_at"],
)
