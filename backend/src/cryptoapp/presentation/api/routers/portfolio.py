from dataclasses import dataclass
from decimal import Decimal
from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Body, Query, UploadFile
from pydantic import BaseModel, Field

from cryptoapp.application.common.id_provider import IdProvider
from cryptoapp.application.portfolio.create import (
    CreatePortfolio,
    CreationPortfolioRequest,
    CreationPortfolioResponse,
)
from cryptoapp.application.portfolio.create_transaction import (
    CreateTransaction,
    TransactionCreationRequest,
)
from cryptoapp.application.portfolio.delete import (
    DeletePortfolio,
    DeletePortfolioRequest,
)
from cryptoapp.application.portfolio.delete_transaction import (
    DeleteTransaction,
    DeleteTransactionRequest,
)
from cryptoapp.application.portfolio.update import (
    UpdatePortfolio,
    UpdatePortfolioRequest,
)
from cryptoapp.application.portfolio.update_transaction import (
    UpdateTransaction,
    UpdateTransactionRequest,
)
from cryptoapp.domain.entities.transaction.transaction import TransactionType
from cryptoapp.infrastructure.persistence.readers.portfolio import (
    PortfolioData,
    PortfolioReader,
    PortfolioStats,
    PortfolioSummary,
    TransactionsPage,
)

portfolio_router = APIRouter(
    prefix="/portfolios", tags=["portfolio"], route_class=DishkaRoute
)


@portfolio_router.post("/", status_code=201)
async def create_portfolio(
    interactor: FromDishka[CreatePortfolio],
    name: Annotated[str, Body()],
    loaded_file: UploadFile | None = None,
) -> CreationPortfolioResponse:
    raw_bytes = loaded_file.file.read() if loaded_file else None
    return await interactor(
        data=CreationPortfolioRequest(name=name, avatar=raw_bytes)
    )


@portfolio_router.patch("/", status_code=204)
async def update_portfolio(
    interactor: FromDishka[UpdatePortfolio],
    portfolio_id: Annotated[int, Body()],
    portfolio_name: Annotated[str | None, Body()] = None,
    loaded_file: UploadFile | None = None,
) -> None:
    raw_bytes = loaded_file.file.read() if loaded_file else None
    await interactor(
        data=UpdatePortfolioRequest(
            portfolio_id=portfolio_id, name=portfolio_name, avatar=raw_bytes
        )
    )


@portfolio_router.get("/summary")
async def get_summary_by_all_portfolios(
    identity_provider: FromDishka[IdProvider],
    reader: FromDishka[PortfolioReader],
) -> PortfolioSummary:
    user_id = await identity_provider.get_current_user_id()
    return await reader.get_portfolio_stats(user_id)


@portfolio_router.delete("/{portfolio_id}")
async def delete_portfolio(
    interactor: FromDishka[DeletePortfolio], portfolio_id: int
) -> dict[str, str]:
    await interactor(data=DeletePortfolioRequest(portfolio_id=portfolio_id))
    return {"message": "Portfolio deleted successfully"}


@portfolio_router.get("/")
async def get_portfolios(
    identity_provider: FromDishka[IdProvider],
    reader: FromDishka[PortfolioReader],
) -> list[PortfolioData]:
    user_id = await identity_provider.get_current_user_id()
    return await reader.get_portfolios_with_presigned_urls(user_id)


@portfolio_router.get("/{portfolio_id}/summary", status_code=200)
async def get_summary_by_portfolio(
    portfolio_id: int,
    identity_provider: FromDishka[IdProvider],
    reader: FromDishka[PortfolioReader],
) -> PortfolioStats:
    user_id = await identity_provider.get_current_user_id()
    return await reader.get_portfolio_stats_by_portfolio_id(
        portfolio_id, user_id
    )


class TransactionCreationSchema(BaseModel):
    asset_id: int

    quantity: Annotated[
        Decimal, Field(max_digits=38, decimal_places=8, gt=Decimal("0"))
    ]
    price: Annotated[
        Decimal | None,
        Field(max_digits=38, decimal_places=12, gt=Decimal("0")),
    ] = None

    transactionType: TransactionType
    note: str | None = None

    fee: Annotated[Decimal | None, Field(max_digits=12, decimal_places=2)] = (
        None
    )

    class Config:
        arbitrary_types_allowed = True


@portfolio_router.post("/{portfolio_id}/transactions", status_code=201)
async def create_transaction_for_portfolio(
    portfolio_id: int,
    data: TransactionCreationSchema,
    interactor: FromDishka[CreateTransaction],
) -> dict[str, int]:
    transaction_id = await interactor(
        data=TransactionCreationRequest(
            portfolio_id=portfolio_id,
            asset_id=data.asset_id,
            quantity=data.quantity,
            price=data.price,
            transactionType=data.transactionType,
            note=data.note,
            fee=data.fee,
        )
    )

    return {"transaction_id": transaction_id}


@portfolio_router.delete("/{portfolio_id}/transactions/{transaction_id}")
async def delete_transaction(
    interactor: FromDishka[DeleteTransaction],
    portfolio_id: int,
    transaction_id: int,
) -> dict[str, str]:
    await interactor(
        data=DeleteTransactionRequest(
            portfolio_id=portfolio_id, transaction_id=transaction_id
        )
    )
    return {"message": "Transaction deleted successfully"}


@dataclass
class UpdateTransactionSchema:
    quantity: Decimal | None
    price: Decimal | None
    note: str | None
    fee: Decimal | None


@portfolio_router.patch(
    "/{portfolio_id}/transactions/{transaction_id}", status_code=204
)
async def update_transaction(
    interactor: FromDishka[UpdateTransaction],
    portfolio_id: int,
    transaction_id: int,
    data: UpdateTransactionSchema,
) -> None:
    await interactor(
        data=UpdateTransactionRequest(
            transaction_id=transaction_id,
            portfolio_id=portfolio_id,
            quantity=data.quantity,
            price=data.price,
            note=data.note,
            fee=data.fee,
        )
    )


@portfolio_router.get("/{portfolio_id}/transactions", status_code=200)
async def get_transactions(
    portfolio_id: int,
    identity_provider: FromDishka[IdProvider],
    reader: FromDishka[PortfolioReader],
    limit: int = Query(default=20, ge=1, description="Max number of records"),
    last_transaction_id: int | None = Query(
        default=None,
        description="ID of the last transaction from previous page "
        "or keyset pagination)",
    ),
) -> TransactionsPage:
    user_id = await identity_provider.get_current_user_id()
    return await reader.get_portfolio_transactions(
        portfolio_id=portfolio_id,
        user_id=user_id,
        limit=limit,
        last_transaction_id=last_transaction_id,
    )
