from decimal import Decimal

import pytest
from cryptoapp.domain.entities.portfolio.portfolio import (
    PortfolioId,
)
from cryptoapp.domain.entities.transaction.transaction import (
    AssetId,
    TransactionType,
)
from cryptoapp.domain.exceptions import EntityNotFound
from cryptoapp.domain.services.transaction import (
    CreateTransactionData,
    TransactionService,
)


@pytest.fixture
def transaction_service(portfolio_repository, transaction_repository):
    return TransactionService(
        portfolio_repository=portfolio_repository,
        transaction_repository=transaction_repository,
    )

@pytest.mark.asyncio
async def test_create_transaction_successful(
    transaction_service, portfolio_repository, transaction_repository
):
    # Arrange
    user_id = 1
    portfolio_id = 2
    portfolio_repository.set_portfolio_exists(portfolio_id, user_id, True)

    data = CreateTransactionData(
        user_id=user_id,
        asset_id=3,
        portfolio_id=portfolio_id,
        quantity=Decimal("5"),
        price=Decimal("200"),
        transaction_type=TransactionType.BUY,
        note="Test transaction",
        fee=Decimal("2.5"),
    )

    # Act
    transaction = await transaction_service.create(data)

    # Assert
    assert transaction is not None
    assert transaction.asset_identity == AssetId(data.asset_id)
    assert transaction.portfolio_id == PortfolioId(data.portfolio_id)
    assert transaction.quantity == data.quantity
    assert transaction.price == data.price
    assert transaction.fee == data.fee
    assert transaction.transaction_type == data.transaction_type
    assert transaction.note == data.note
    assert len(transaction_repository._transactions) == 1


@pytest.mark.asyncio
async def test_create_transaction_portfolio_not_found(
    transaction_service, portfolio_repository, transaction_repository
):
    # Arrange
    user_id = 1
    portfolio_id = 2
    portfolio_repository.set_portfolio_exists(portfolio_id, user_id, False)

    data = CreateTransactionData(
        user_id=user_id,
        asset_id=3,
        portfolio_id=portfolio_id,
        quantity=Decimal("5"),
        price=Decimal("200"),
        transaction_type=TransactionType.BUY,
        note="Test transaction",
        fee=Decimal("2.5"),
    )

    # Act & Assert
    with pytest.raises(EntityNotFound):
        await transaction_service.create(data)

    assert len(transaction_repository._transactions) == 0

@pytest.mark.asyncio
async def test_create_transaction_with_minimal_data(
    transaction_service, portfolio_repository, transaction_repository
):
    # Arrange
    user_id = 1
    portfolio_id = 2
    portfolio_repository.set_portfolio_exists(portfolio_id, user_id, True)

    data = CreateTransactionData(
        user_id=user_id,
        asset_id=3,
        portfolio_id=portfolio_id,
        quantity=Decimal("5"),
        price=None,
        transaction_type=TransactionType.OUT,
        note=None,
        fee=None,
    )

    transaction = await transaction_service.create(data)

    assert transaction is not None
    assert transaction.price is None
    assert transaction.note is None
    assert transaction.fee is None
    assert transaction.transaction_type == TransactionType.OUT
    assert len(transaction_repository._transactions) == 1

@pytest.mark.asyncio
async def test_create_sell_transaction(
    transaction_service, portfolio_repository, transaction_repository
):
    # Arrange
    user_id = 1
    portfolio_id = 2
    portfolio_repository.set_portfolio_exists(portfolio_id, user_id, True)

    data = CreateTransactionData(
        user_id=user_id,
        asset_id=3,
        portfolio_id=portfolio_id,
        quantity=Decimal("5"),
        price=Decimal("200"),
        transaction_type=TransactionType.SELL,
        note="Selling some assets",
        fee=Decimal("2.5"),
    )

    # Act
    transaction = await transaction_service.create(data)

    # Assert
    assert transaction is not None
    assert transaction.transaction_type == TransactionType.SELL
    assert transaction.note == "Selling some assets"
    assert len(transaction_repository._transactions) == 1
