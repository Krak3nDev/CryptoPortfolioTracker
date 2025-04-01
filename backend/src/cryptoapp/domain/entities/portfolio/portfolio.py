from dataclasses import dataclass

from cryptoapp.domain.entities.identity import Identity
from cryptoapp.domain.entities.transaction.transaction import Transaction, TransactionId
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

    @property
    def avatar(self) -> str:
        return self._avatar

    def get_transactions(self) -> tuple[Transaction, ...]:
        return tuple(self._transactions)

    def add_transaction(self, transaction: Transaction) -> None:
        self._transactions.append(transaction)

    def remove_transaction(self, transaction_id: TransactionId) -> None:
        for transaction in self._transactions:
            if transaction.identity == transaction_id:
                self._transactions.remove(transaction)
                return

        raise EntityNotFound(field_name="Transaction", value=transaction_id.value)
