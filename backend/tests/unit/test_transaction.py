from decimal import Decimal

import pytest
from cryptoapp.domain.entities.transaction.transaction import (
    Transaction,
    TransactionType,
    CreationData,
)
from cryptoapp.domain.exceptions import DomainError
from cryptoapp.domain.services.transaction import CreateTransactionData


def test_create_buy_transaction():
    data = CreationData(
        asset_id=1,
        quantity=Decimal("10"),
        price=Decimal("100.50"),
        transaction_type=TransactionType.BUY,
        note="Initial note",
        fee=Decimal("0.5"),
        portfolio_id=12
    )

    tx = Transaction.create(data)

    assert tx.identity._value is None
    assert tx._asset_id.value == 1
    assert tx.quantity == Decimal("10")
    assert tx.price == Decimal("100.50")
    assert tx.transaction_type == TransactionType.BUY
    assert tx.note == "Initial note"
    assert tx.fee == Decimal("0.5")



def test_cannot_set_price_for_in_transaction():
    data = CreationData(
        asset_id=3,
        quantity=Decimal("5"),
        price=None,
        transaction_type=TransactionType.IN,
        note=None,
        fee=None,
        portfolio_id=12
    )
    tx = Transaction.create(data)

    with pytest.raises(DomainError) as exc_info:
        tx.price = Decimal("999.99")

    assert "Cannot set price for a transfer_in transaction." in str(
        exc_info.value
    )


def test_cannot_set_price_for_out_transaction():
    data = CreationData(
        asset_id=4,
        quantity=Decimal("2"),
        price=None,
        transaction_type=TransactionType.OUT,
        note=None,
        fee=None,
        portfolio_id=12
    )
    tx = Transaction.create(data)

    with pytest.raises(DomainError) as exc_info:
        tx.price = Decimal("123.45")

    assert "Cannot set price for a transfer_out transaction." in str(
        exc_info.value
    )



