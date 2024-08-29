from datetime import datetime
from decimal import Decimal
from enum import Enum

from sqlalchemy import BIGINT, Integer, ForeignKey, DECIMAL, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from cryptoapp.infrastructure.database.models import Base
from cryptoapp.infrastructure.database.models.base import TimestampMixin


class TransactionType(str, Enum):
    BUY = "buy"
    SELL = "sell"


class TransactionDB(Base, TimestampMixin):
    __tablename__ = "transactions"
    transaction_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(BIGINT, ForeignKey("users.user_id"))
    quantity: Mapped[Decimal] = mapped_column(DECIMAL(precision=10, scale=2))
    price_per_unit: Mapped[Decimal] = mapped_column(DECIMAL(precision=10, scale=2))
    transaction_type: Mapped[TransactionType]
    transaction_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
