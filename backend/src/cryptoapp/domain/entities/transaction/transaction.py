from dataclasses import dataclass
from decimal import Decimal
from enum import Enum

from cryptoapp.domain.entities.identity import Identity
from cryptoapp.domain.exceptions import DomainError


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
    asset_id: int
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
            _asset_id=AssetId(data.asset_id),
            _quantity=data.quantity,
            _price=data.price,
            _transaction_type=data.transaction_type,
            _note=data.note,
            _fee=data.fee,
        )

    @property
    def transaction_type(self) -> TransactionType:
        return self._transaction_type

    @property
    def identity(self) -> TransactionId:
        return self._identity

    @property
    def price(self) -> Decimal | None:
        return self._price

    @price.setter
    def price(self, value: Decimal) -> None:
        if self._transaction_type in (TransactionType.IN, TransactionType.OUT):
            raise DomainError(
                f"Cannot set price for a {self._transaction_type.value} "
                "transaction."
            )
        self._price = value

    @property
    def quantity(self) -> Decimal:
        return self._quantity

    @quantity.setter
    def quantity(self, value: Decimal) -> None:
        self._quantity = value

    @property
    def note(self) -> str | None:
        return self._note

    @note.setter
    def note(self, value: str | None) -> None:
        self._note = value

    @property
    def fee(self) -> Decimal | None:
        return self._fee

    @fee.setter
    def fee(self, value: Decimal | None) -> None:
        self._fee = value
