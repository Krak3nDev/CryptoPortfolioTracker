from dataclasses import dataclass
from decimal import Decimal
from enum import Enum

from cryptoapp.domain.entities.identity import Identity


class TransactionType(str, Enum):
    BUY = "buy"
    SELL = "sell"
    IN = "transfer_in"
    OUT = "transfer_out"


class TransactionId(Identity):
    pass


class AssetId(Identity):
    pass


@dataclass
class CreateTransactionData:
    asset_id: AssetId
    quantity: Decimal
    price: Decimal | None
    transaction_type: TransactionType
    note: str | None
    fee: Decimal | None


@dataclass
class Transaction:
    _identity: TransactionId
    _asset_id: AssetId
    _quantity: Decimal
    _price: Decimal | None
    _transaction_type: TransactionType
    _note: str | None
    _fee: Decimal | None

    @classmethod
    def create(cls, data: CreateTransactionData) -> "Transaction":
        return cls(
            _identity=TransactionId(None),
            _asset_id=data.asset_id,
            _quantity=data.quantity,
            _price=data.price,
            _transaction_type=data.transaction_type,
            _note=data.note,
            _fee=data.fee,
        )

    @property
    def identity(self) -> TransactionId:
        return self._identity
