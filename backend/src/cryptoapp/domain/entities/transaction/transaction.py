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
class Transaction:
    _identity: TransactionId
    _asset_id: AssetId
    _quantity: Decimal
    _price: Decimal | None
    _transaction_type: TransactionType
    _note: str | None
    _fee: Decimal | None

    @property
    def identity(self) -> int:
        return self._identity.value
