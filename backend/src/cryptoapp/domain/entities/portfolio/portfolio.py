from dataclasses import dataclass
from decimal import Decimal

from cryptoapp.domain.entities.identity import Identity
from cryptoapp.domain.entities.transaction.transaction import (
    CreateTransactionData,
    Transaction,
    TransactionId,
)
from cryptoapp.domain.entities.user.user import UserId
from cryptoapp.domain.exceptions import EntityNotFound


class PortfolioId(Identity):
    pass


@dataclass
class Portfolio:
    _identity: PortfolioId
    _user_id: UserId
    _name: str
    _avatar: str
    _transactions: list[Transaction]

    @classmethod
    def create(
        cls,
        portfolio_id: int | None,
        user_id: int,
        name: str,
        avatar: str,
    ) -> "Portfolio":
        return cls(
            _identity=PortfolioId(portfolio_id),
            _user_id=UserId(user_id),
            _name=name,
            _avatar=avatar,
            _transactions=[],
        )

    @property
    def identity(self) -> PortfolioId:
        return self._identity

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def avatar(self) -> str:
        return self._avatar

    @avatar.setter
    def avatar(self, value: str) -> None:
        self._avatar = value

    def get_transaction(self, transaction_id: TransactionId) -> Transaction:
        for transaction in self._transactions:
            if transaction.identity == transaction_id:
                return transaction

        raise EntityNotFound(
            field_name="Transaction", value=transaction_id.value
        )

    def add_transaction(self, data: CreateTransactionData) -> TransactionId:
        transaction = Transaction.create(data)
        self._transactions.append(transaction)
        return transaction.identity

    def remove_transaction(self, transaction_id: TransactionId) -> None:
        for transaction in self._transactions:
            if transaction.identity == transaction_id:
                self._transactions.remove(transaction)
                return

        raise EntityNotFound(
            field_name="Transaction", value=transaction_id.value
        )

    def update_transaction(
        self,
        transaction_id: TransactionId,
        quantity: Decimal | None = None,
        price: Decimal | None = None,
        note: str | None = None,
        fee: Decimal | None = None,
    ) -> None:
        transaction = self.get_transaction(transaction_id)

        if quantity is not None:
            transaction.quantity = quantity

        if price is not None:
            transaction.price = price

        if note is not None:
            transaction.note = note

        if fee is not None:
            transaction.fee = fee
