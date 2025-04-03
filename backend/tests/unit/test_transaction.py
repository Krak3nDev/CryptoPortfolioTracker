from decimal import Decimal

import pytest
from cryptoapp.domain.entities.transaction.transaction import (
    CreateTransactionData,
    Transaction,
    TransactionType,
)
from cryptoapp.domain.exceptions import DomainError


def test_create_buy_transaction():
    data = CreateTransactionData(
        asset_id=1,
        quantity=Decimal("10"),
        price=Decimal("100.50"),
        transaction_type=TransactionType.BUY,
        note="Initial note",
        fee=Decimal("0.5")
    )

    tx = Transaction.create(data)

    assert tx.identity._value is None
    assert tx._asset_id.value == 1
    assert tx.quantity == Decimal("10")
    assert tx.price == Decimal("100.50")
    assert tx.transaction_type == TransactionType.BUY
    assert tx.note == "Initial note"
    assert tx.fee == Decimal("0.5")


def test_create_in_transaction_has_no_price():
    data = CreateTransactionData(
        asset_id=2,
        quantity=Decimal("5"),
        price=None,
        transaction_type=TransactionType.IN,
        note=None,
        fee=None
    )
    tx = Transaction.create(data)

    assert tx.transaction_type == TransactionType.IN
    assert tx.price is None


def test_cannot_set_price_for_in_transaction():
    data = CreateTransactionData(
        asset_id=3,
        quantity=Decimal("5"),
        price=None,
        transaction_type=TransactionType.IN,
        note=None,
        fee=None
    )
    tx = Transaction.create(data)

    with pytest.raises(DomainError) as exc_info:
        tx.price = Decimal("999.99")

    assert "Cannot set price for a transfer_in transaction." in str(exc_info.value)


def test_cannot_set_price_for_out_transaction():
    data = CreateTransactionData(
        asset_id=4,
        quantity=Decimal("2"),
        price=None,
        transaction_type=TransactionType.OUT,
        note=None,
        fee=None
    )
    tx = Transaction.create(data)

    with pytest.raises(DomainError) as exc_info:
        tx.price = Decimal("123.45")

    assert "Cannot set price for a transfer_out transaction." in str(exc_info.value)


def test_set_quantity():
    data = CreateTransactionData(
        asset_id=10,
        quantity=Decimal("1.23"),
        price=Decimal("456.78"),
        transaction_type=TransactionType.SELL,
        note=None,
        fee=Decimal("0.05")
    )
    tx = Transaction.create(data)

    tx.quantity = Decimal("2.34")
    assert tx.quantity == Decimal("2.34")


def test_set_note():
    data = CreateTransactionData(
        asset_id=11,
        quantity=Decimal("1"),
        price=Decimal("100"),
        transaction_type=TransactionType.BUY,
        note=None,
        fee=None
    )
    tx = Transaction.create(data)

    tx.note = "New note"
    assert tx.note == "New note"


def test_set_fee():
    data = CreateTransactionData(
        asset_id=12,
        quantity=Decimal("10"),
        price=Decimal("500"),
        transaction_type=TransactionType.BUY,
        note="Fee test",
        fee=Decimal("0.1")
    )
    tx = Transaction.create(data)

    tx.fee = Decimal("0.15")
    assert tx.fee == Decimal("0.15")
