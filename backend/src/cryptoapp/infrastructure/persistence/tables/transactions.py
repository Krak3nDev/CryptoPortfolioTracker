from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Table,
    text,
)
from sqlalchemy.orm import composite

from cryptoapp.domain.entities.transaction.transaction import (
    AssetId,
    Transaction,
    TransactionId,
)
from cryptoapp.infrastructure.persistence.tables.base import mapper_registry

transactions_table = Table(
    "transactions",
    mapper_registry.metadata,
    Column("transaction_id", Integer, primary_key=True, autoincrement=True),
    Column(
        "portfolio_id",
        Integer,
        ForeignKey("portfolios.portfolio_id", ondelete="CASCADE"),
        nullable=False,
    ),
    Column(
        "asset_id",
        Integer,
        ForeignKey("assets.asset_id", ondelete="CASCADE"),
        nullable=False,
    ),
    Column("note", String(255), nullable=True),
    Column(
        "transaction_type", String(20), nullable=False
    ),  # "buy"/"sell"/"transfer_in"/"transfer_out"
    Column("fee", Numeric(12, 2), nullable=True),
    Column("quantity", Numeric(38, 8), nullable=False),  #
    Column("price", Numeric(38, 12), nullable=True),
    Column(
        "created_at",
        DateTime(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    ),
)

mapper_registry.map_imperatively(
    Transaction,
    transactions_table,
    properties={
        "_identity": composite(TransactionId, transactions_table.c.transaction_id),
        "_asset_id": composite(AssetId, transactions_table.c.asset_id),
        "_quantity": transactions_table.c.quantity,
        "_price": transactions_table.c.price,
        "_transaction_type": transactions_table.c.transaction_type,
        "_note": transactions_table.c.note,
        "_fee": transactions_table.c.fee,
    },
    exclude_properties=["created_at"],
)
