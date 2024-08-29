from datetime import datetime
from decimal import Decimal

from sqlalchemy import Integer, String, DateTime, Float, DECIMAL
from sqlalchemy.orm import mapped_column, Mapped

from .base import Base, TimestampMixin


class AssetDB(Base, TimestampMixin):
    __tablename__ = "assets"
    crypto_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=False
    )
    name: Mapped[str] = mapped_column(String(64))
    symbol: Mapped[str] = mapped_column(String(64))
    slug: Mapped[str] = mapped_column(String(64))
    cmc_rank: Mapped[int] = mapped_column(Integer)
    price: Mapped[Decimal] = mapped_column(DECIMAL(precision=18, scale=8))
    percent_change_1h: Mapped[float] = mapped_column(Float)
    percent_change_24h: Mapped[float] = mapped_column(Float)
    percent_change_7d: Mapped[float] = mapped_column(Float)
    last_updated: Mapped[datetime] = mapped_column(DateTime(timezone=True))
