from dataclasses import dataclass

from cryptoapp.domain.entities.identity import Identity
from cryptoapp.domain.entities.transaction.transaction import Transaction
from cryptoapp.domain.entities.user.user import UserId
from cryptoapp.domain.exceptions import TransactionNotFound


class PortfolioId(Identity):
    pass


@dataclass
class Portfolio:
    _identity: PortfolioId
    _user_id: UserId
    _name: str
    _avatar: str
    _transactions: list[Transaction]

    @property
    def identity(self) -> int:
        return self._identity.value

    @property
    def name(self) -> str:
        return self._name

    @property
    def avatar(self) -> str:
        return self._avatar

    def get_transactions(self) -> list[Transaction]:
        return self._transactions

    def add_transaction(self, transaction: Transaction) -> None:
        self._transactions.append(transaction)

    def remove_transaction(self, transaction_id: int) -> None:
        for transaction in self._transactions:
            if transaction.identity == transaction_id:
                self._transactions.remove(transaction)
                return

        raise TransactionNotFound(transaction_id=transaction_id)
