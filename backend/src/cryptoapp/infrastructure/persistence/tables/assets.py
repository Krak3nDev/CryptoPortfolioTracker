from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String,
    Table,
    Boolean,
    Numeric,
    text,
)

from cryptoapp.infrastructure.persistence.tables.base import mapper_registry

assets_table = Table(
    "assets",
    mapper_registry.metadata,
    Column("asset_id", Integer, primary_key=True, autoincrement=True),
    Column("cmc_id", Integer, nullable=True, unique=True),
    Column("name", String(255), nullable=False),
    Column("symbol", String(50), nullable=False),
    Column("slug", String(255), nullable=True),
    Column("date_added", DateTime(timezone=True), nullable=True),
    Column("is_infinite_supply", Boolean, nullable=False, server_default="0"),
    Column("max_supply", Numeric(38, 6), nullable=True),
    Column("total_supply", Numeric(38, 6), nullable=True),
    Column("circulating_supply", Numeric(38, 6), nullable=True),
    Column("price_usd", Numeric(38, 12), nullable=True),
    Column("volume_24h_usd", Numeric(38, 2), nullable=True),
    Column("market_cap_usd", Numeric(38, 2), nullable=True),
    Column("percent_change_1h_usd", Numeric(15, 5), nullable=True),
    Column("percent_change_24h_usd", Numeric(15, 5), nullable=True),
    Column("percent_change_7d_usd", Numeric(15, 5), nullable=True),
    Column("last_updated", DateTime(timezone=True), nullable=False),
    Column(
        "created_at",
        DateTime(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    ),
)
