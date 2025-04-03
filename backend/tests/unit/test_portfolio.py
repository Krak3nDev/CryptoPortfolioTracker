from decimal import Decimal

import pytest
from cryptoapp.domain.entities.portfolio.portfolio import Portfolio
from cryptoapp.domain.entities.transaction.transaction import (
    CreateTransactionData,
    TransactionId,
    TransactionType,
)
from cryptoapp.domain.entities.user.user import UserId
from cryptoapp.domain.exceptions import EntityNotFound


@pytest.fixture
def portfolio():
    return Portfolio.create(
        portfolio_id=None,
        user_id=100,
        name="My Portfolio",
        avatar="avatar_url"
    )


def test_portfolio_creation(portfolio):
    assert portfolio.identity._value is None
    assert portfolio._user_id == UserId(100)
    assert portfolio.name == "My Portfolio"
    assert portfolio.avatar == "avatar_url"
    assert len(portfolio._transactions) == 0


def test_add_transaction(portfolio):
    data = CreateTransactionData(
        asset_id=1,
        quantity=Decimal("5"),
        price=Decimal("100.0"),
        transaction_type=TransactionType.BUY,
        note="Some note",
        fee=Decimal("0.1")
    )
    transaction_id = portfolio.add_transaction(data)

    assert len(portfolio._transactions) == 1
    transaction = portfolio._transactions[0]
    assert transaction.identity == transaction_id
    assert transaction.quantity == Decimal("5")
    assert transaction.price == Decimal("100.0")
    assert transaction.note == "Some note"
    assert transaction.fee == Decimal("0.1")


def test_get_transaction(portfolio):
    data = CreateTransactionData(
        asset_id=2,
        quantity=Decimal("10"),
        price=Decimal("50.0"),
        transaction_type=TransactionType.SELL,
        note=None,
        fee=None
    )
    transaction_id = portfolio.add_transaction(data)

    found_tx = portfolio.get_transaction(transaction_id)
    assert found_tx.identity == transaction_id
    assert found_tx._transaction_type == TransactionType.SELL


def test_get_transaction_not_found(portfolio):
    fake_id = TransactionId(999)
    with pytest.raises(EntityNotFound) as exc_info:
        portfolio.get_transaction(fake_id)

    assert "Transaction" in str(exc_info.value)


def test_remove_transaction(portfolio):
    data = CreateTransactionData(
        asset_id=3,
        quantity=Decimal("1.5"),
        price=None,
        transaction_type=TransactionType.IN,
        note="Transfer in",
        fee=None
    )
    transaction_id = portfolio.add_transaction(data)
    assert len(portfolio._transactions) == 1

    portfolio.remove_transaction(transaction_id)
    assert len(portfolio._transactions) == 0


def test_remove_transaction_not_found(portfolio):
    fake_id = TransactionId(111)
    with pytest.raises(EntityNotFound) as exc_info:
        portfolio.remove_transaction(fake_id)

    assert "Transaction" in str(exc_info.value)


def test_update_transaction(portfolio):
    data = CreateTransactionData(
        asset_id=4,
        quantity=Decimal("2"),
        price=Decimal("10"),
        transaction_type=TransactionType.BUY,
        note="Old note",
        fee=Decimal("0.05")
    )
    transaction_id = portfolio.add_transaction(data)

    new_quantity = Decimal("3")
    new_price = Decimal("12.5")
    new_note = "Updated note"
    new_fee = Decimal("0.1")

    portfolio.update_transaction(
        transaction_id=transaction_id,
        quantity=new_quantity,
        price=new_price,
        note=new_note,
        fee=new_fee
    )

    tx = portfolio.get_transaction(transaction_id)
    assert tx.quantity == new_quantity
    assert tx.price == new_price
    assert tx.note == new_note
    assert tx.fee == new_fee
