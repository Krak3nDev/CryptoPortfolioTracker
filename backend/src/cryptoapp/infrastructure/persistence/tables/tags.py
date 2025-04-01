from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Table,
)

from cryptoapp.infrastructure.persistence.tables.base import mapper_registry

tags_table = Table(
    "tags",
    mapper_registry.metadata,
    Column("tag_id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(255), nullable=False, unique=True),
)

assets_tags_table = Table(
    "assets_tags",
    mapper_registry.metadata,
    Column(
        "asset_id",
        Integer,
        ForeignKey("assets.asset_id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "tag_id",
        Integer,
        ForeignKey("tags.tag_id", ondelete="CASCADE"),
        primary_key=True,
    ),
)
