from typing import Optional

import pytest
from cryptoapp.domain.entities.portfolio.portfolio import (
    Portfolio,
    PortfolioId,
)
from cryptoapp.domain.entities.portfolio.repository import PortfolioRepository
from cryptoapp.domain.entities.transaction.repository import (
    TransactionRepository,
)
from cryptoapp.domain.entities.transaction.transaction import (
    Transaction,
    TransactionId,
)
from cryptoapp.domain.entities.user.gateway import (
    UserAvailabilityInfo,
    UserGateway,
)
from cryptoapp.domain.entities.user.user import User, UserId


@pytest.fixture(scope="function")
def user():
    return User.create(
        user_id=1,
        email="test@example.com",
        hashed_password="hashed_password",
        username="testuser",
    )


@pytest.fixture(scope="function")
def user_gateway():
    class InMemoryUserGateway(UserGateway):
        def __init__(self):
            self._users = {}

        async def by_identity(self, user_id: UserId) -> User | None:
            return self._users.get(user_id)

        async def by_username(self, username: str) -> User | None:
            for user in self._users.values():
                if user.username == username:
                    return user
            return None

        async def get_username_email_availability(
            self, username: str, email: str
        ) -> UserAvailabilityInfo | None:
            for u in self._users.values():
                if u.username == username or u.email == email:
                    return {"username": u.username, "email": u.email}
            return None

        def add(self, user: User) -> None:
            self._users[user.identity] = user

    return InMemoryUserGateway()


@pytest.fixture(scope="function")
def portfolio_repository():
    class InMemoryPortfolioRepository(PortfolioRepository):
        def __init__(self):
            self._portfolios = {}
            self._portfolio_exists = {}
            self._next_id = 1

        async def by_identity(
            self, portfolio_id: PortfolioId, user_id: UserId
        ) -> Portfolio | None:
            key = (portfolio_id, user_id)
            return self._portfolios.get(key)

        async def is_exists(
            self, portfolio_id: PortfolioId, user_id: UserId
        ) -> bool:
            key = (portfolio_id, user_id)
            return self._portfolio_exists.get(key, False)

        def add(self, portfolio: Portfolio) -> None:
            key = PortfolioId(self._next_id)
            self._next_id += 1
            self._portfolios[key] = portfolio

        async def delete(self, portfolio: Portfolio) -> None:
            if portfolio.identity in self._portfolios:
                del self._portfolios[portfolio.identity]

        def set_portfolio_exists(
            self, portfolio_id: int, user_id: int, exists: bool
        ):
            self._portfolio_exists[
                (PortfolioId(portfolio_id), UserId(user_id))
            ] = exists

    return InMemoryPortfolioRepository()


@pytest.fixture(scope="function")
def transaction_repository():
    class InMemoryTransactionRepository(TransactionRepository):
        def __init__(self):
            self._transactions = {}
            self._next_id = 1

        def add(self, transaction: Transaction) -> Transaction:
            object_dict = {
                "_identity": TransactionId(self._next_id),
                "_asset_id": transaction.asset_identity,
                "_portfolio_id": transaction.portfolio_id,
                "_quantity": transaction.quantity,
                "_price": transaction.price,
                "_transaction_type": transaction.transaction_type,
                "_note": transaction.note,
                "_fee": transaction.fee,
            }

            tx = Transaction(**object_dict)
            self._transactions[tx.identity] = tx
            self._next_id += 1
            return tx

        async def delete(self, transaction: Transaction) -> None:
            if transaction.identity in self._transactions:
                del self._transactions[transaction.identity]

        async def by_identity(
            self,
            transaction_id: TransactionId,
            portfolio_id: PortfolioId,
            user_id: UserId,
        ) -> Optional[Transaction]:
            transaction = self._transactions.get(transaction_id)
            if transaction and transaction.portfolio_id == portfolio_id:
                return transaction
            return None

    return InMemoryTransactionRepository()
