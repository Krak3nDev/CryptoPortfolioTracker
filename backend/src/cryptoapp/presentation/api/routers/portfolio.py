from decimal import Decimal
from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Form, UploadFile, Query
from pydantic import BaseModel, Field

from cryptoapp.application.common.id_provider import IdProvider
from cryptoapp.application.portfolio.create import (
    CreatePortfolio,
    CreationPortfolioRequest,
    CreationPortfolioResponse,
)
from cryptoapp.application.portfolio.create_transaction import (
    TransactionCreationRequest,
    CreateTransaction,
)
from cryptoapp.domain.entities.transaction.transaction import TransactionType
from cryptoapp.infrastructure.persistence.readers.portfolio import (
    PortfolioReader,
    PortfolioData,
    TransactionData,
)

portfolio_router = APIRouter(
    prefix="/portfolios", tags=["portfolio"], route_class=DishkaRoute
)


@portfolio_router.post("/", status_code=201)
async def create_portfolio(
    interactor: FromDishka[CreatePortfolio],
    name: Annotated[str, Form(...)],
    loaded_file: UploadFile | None = None,
) -> CreationPortfolioResponse:
    raw_bytes = loaded_file.file.read() if loaded_file else None
    return await interactor(data=CreationPortfolioRequest(name=name, avatar=raw_bytes))


@portfolio_router.get("/", response_model_exclude_none=True)
async def get_portfolios(
    identity_provider: FromDishka[IdProvider], reader: FromDishka[PortfolioReader]
) -> list[PortfolioData]:
    user_id = await identity_provider.get_current_user_id()
    return await reader.get_portfolios_with_presigned_urls(user_id)


class TransactionCreationSchema(BaseModel):
    asset_id: int

    quantity: Annotated[
        Decimal, Field(max_digits=38, decimal_places=8, gt=Decimal("0"))
    ]
    price: Annotated[
        Decimal | None, Field(max_digits=38, decimal_places=12, gt=Decimal("0"))
    ] = None

    transactionType: TransactionType
    note: str | None = None

    fee: Annotated[Decimal | None, Field(max_digits=12, decimal_places=2)] = None

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


@portfolio_router.get("/{portfolio_id}/transactions", status_code=200)
async def get_transactions(
    portfolio_id: int,
    identity_provider: FromDishka[IdProvider],
    reader: FromDishka[PortfolioReader],
    limit: int = Query(
        default=20, ge=1, description="The maximum number of records per page"
    ),
    offset: int = Query(
        default=0, ge=0, description="Offset from the beginning of the selection"
    ),
) -> list[TransactionData]:
    user_id = await identity_provider.get_current_user_id()
    return await reader.get_portfolio_transactions(
        portfolio_id=portfolio_id, user_id=user_id, limit=limit, offset=offset
    )
