from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Table,
    text,
)
from sqlalchemy.orm import composite, relationship

from cryptoapp.domain.entities.portfolio.portfolio import Portfolio, PortfolioId
from cryptoapp.domain.entities.transaction.transaction import Transaction
from cryptoapp.domain.entities.user.user import UserId
from cryptoapp.infrastructure.persistence.tables.base import mapper_registry

portfolios_table = Table(
    "portfolios",
    mapper_registry.metadata,
    Column("portfolio_id", Integer, primary_key=True, autoincrement=True),
    Column(
        "user_id",
        Integer,
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False,
    ),
    Column("name", String(50), nullable=False),
    Column("avatar", String(255), nullable=False),
    Column(
        "created_at",
        DateTime(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    ),
)

mapper_registry.map_imperatively(
    Portfolio,
    portfolios_table,
    properties={
        "_identity": composite(PortfolioId, portfolios_table.c.portfolio_id),
        "_user_id": composite(UserId, portfolios_table.c.user_id),
        "_name": portfolios_table.c.name,
        "_avatar": portfolios_table.c.avatar,
        "_transactions": relationship(
            Transaction, cascade="all, delete-orphan", lazy="joined"
        ),
    },
    exclude_properties=["created_at"],
)
