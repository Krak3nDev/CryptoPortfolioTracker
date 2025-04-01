from decimal import Decimal
from typing import Sequence, TypedDict

from sqlalchemy import case, func, literal, select, union_all
from sqlalchemy.ext.asyncio import AsyncSession

from cryptoapp.domain.entities.transaction.transaction import TransactionType
from cryptoapp.infrastructure.persistence.gateways.base import SessionInitializer
from cryptoapp.infrastructure.persistence.tables import (
    assets_table,
    portfolios_table,
    transactions_table,
)
from cryptoapp.infrastructure.services.minio import S3Minio


class PortfolioData(TypedDict):
    portfolio_name: str
    portfolio_id: int | None
    avatar: str | None
    total_value: Decimal
    value_change_24h: Decimal
    percent_change_24h: Decimal


class TransactionData(TypedDict):
    transaction_id: int
    transaction_type: TransactionType
    transaction_time: str
    quantity: Decimal
    asset_id: int
    asset_symbol: str
    asset_name: str
    purchase_price: Decimal | None
    current_price: Decimal
    note: str | None


class PortfolioReader(SessionInitializer):
    def __init__(self, session: AsyncSession, minio: S3Minio):
        super().__init__(session)
        self._minio = minio

    async def _get_portfolios(self, user_id: int) -> Sequence[PortfolioData]:
        user_portfolios = (
            select(
                portfolios_table.c.portfolio_id,
                portfolios_table.c.name.label("portfolio_name"),
                portfolios_table.c.avatar,
            )
            .where(portfolios_table.c.user_id == user_id)
            .cte("user_portfolios")
        )

        portfolio_assets = (
            select(
                portfolios_table.c.portfolio_id,
                portfolios_table.c.name.label("portfolio_name"),
                portfolios_table.c.avatar,
                assets_table.c.asset_id,
                assets_table.c.symbol,
                assets_table.c.name.label("asset_name"),
                func.sum(
                    case(
                        (
                            transactions_table.c.transaction_type == "buy",
                            transactions_table.c.quantity,
                        ),
                        (
                            transactions_table.c.transaction_type == "sell",
                            -transactions_table.c.quantity,
                        ),
                        (
                            transactions_table.c.transaction_type == "transfer_in",
                            transactions_table.c.quantity,
                        ),
                        (
                            transactions_table.c.transaction_type == "transfer_out",
                            -transactions_table.c.quantity,
                        ),
                        else_=0,
                    )
                ).label("total_quantity"),
                assets_table.c.price_usd.label("current_price"),
                (
                    assets_table.c.price_usd * func.sum(transactions_table.c.quantity)
                ).label("current_value"),
                (
                    assets_table.c.price_usd
                    * func.sum(transactions_table.c.quantity)
                    * assets_table.c.percent_change_24h_usd
                    / 100
                ).label("value_change_24h"),
                assets_table.c.percent_change_24h_usd.label("percent_change_24h"),
            )
            .select_from(
                portfolios_table.join(
                    transactions_table,
                    portfolios_table.c.portfolio_id
                    == transactions_table.c.portfolio_id,
                ).join(
                    assets_table,
                    transactions_table.c.asset_id == assets_table.c.asset_id,
                )
            )
            .where(portfolios_table.c.user_id == user_id)
            .group_by(
                portfolios_table.c.portfolio_id,
                portfolios_table.c.name,
                portfolios_table.c.avatar,
                assets_table.c.asset_id,
                assets_table.c.symbol,
                assets_table.c.name,
                assets_table.c.price_usd,
                assets_table.c.percent_change_24h_usd,
            )
            .cte("portfolio_assets")
        )

        portfolio_totals_with_transactions = (
            select(
                portfolio_assets.c.portfolio_id,
                portfolio_assets.c.portfolio_name,
                portfolio_assets.c.avatar,
                func.sum(portfolio_assets.c.current_value).label("total_value"),
                func.sum(portfolio_assets.c.value_change_24h).label("value_change_24h"),
                case(
                    (
                        func.sum(portfolio_assets.c.current_value) > 0,
                        func.sum(portfolio_assets.c.value_change_24h)
                        / func.sum(portfolio_assets.c.current_value)
                        * 100,
                    ),
                    else_=0,
                ).label("percent_change_24h"),
            )
            .group_by(
                portfolio_assets.c.portfolio_id,
                portfolio_assets.c.portfolio_name,
                portfolio_assets.c.avatar,
            )
            .cte("portfolio_totals_with_transactions")
        )

        all_user_portfolios = (
            select(
                user_portfolios.c.portfolio_id,
                user_portfolios.c.portfolio_name,
                user_portfolios.c.avatar,
                func.coalesce(
                    portfolio_totals_with_transactions.c.total_value, 0
                ).label("total_value"),
                func.coalesce(
                    portfolio_totals_with_transactions.c.value_change_24h, 0
                ).label("value_change_24h"),
                func.coalesce(
                    portfolio_totals_with_transactions.c.percent_change_24h, 0
                ).label("percent_change_24h"),
                literal(1).label("sort_order"),
            )
            .select_from(
                user_portfolios.outerjoin(
                    portfolio_totals_with_transactions,
                    user_portfolios.c.portfolio_id
                    == portfolio_totals_with_transactions.c.portfolio_id,
                )
            )
            .cte("all_user_portfolios")
        )

        all_portfolios_total = select(
            func.sum(all_user_portfolios.c.total_value).label("total_value"),
            func.sum(all_user_portfolios.c.value_change_24h).label("value_change_24h"),
            case(
                (
                    func.sum(all_user_portfolios.c.total_value) > 0,
                    func.sum(all_user_portfolios.c.value_change_24h)
                    / func.sum(all_user_portfolios.c.total_value)
                    * 100,
                ),
                else_=0,
            ).label("percent_change_24h"),
        ).cte("all_portfolios_total")

        all_portfolios_query = select(
            literal("All Portfolios").label("portfolio_name"),
            literal(None).label("portfolio_id"),
            literal("").label("avatar"),
            all_portfolios_total.c.total_value,
            all_portfolios_total.c.value_change_24h,
            all_portfolios_total.c.percent_change_24h,
            literal(0).label("sort_order"),
        )

        individual_portfolios_query = select(
            all_user_portfolios.c.portfolio_name,
            all_user_portfolios.c.portfolio_id,
            all_user_portfolios.c.avatar,
            all_user_portfolios.c.total_value,
            all_user_portfolios.c.value_change_24h,
            all_user_portfolios.c.percent_change_24h,
            all_user_portfolios.c.sort_order,
        )

        combined_query = union_all(
            all_portfolios_query, individual_portfolios_query
        ).alias("combined")

        final_query = (
            select(
                combined_query.c.portfolio_name,
                combined_query.c.portfolio_id,
                combined_query.c.avatar,
                combined_query.c.total_value,
                combined_query.c.value_change_24h,
                combined_query.c.percent_change_24h,
            )
            .select_from(combined_query)
            .order_by(combined_query.c.sort_order, combined_query.c.portfolio_id)
        )

        result = await self._session.execute(final_query)
        rows = result.mappings().all()

        return [
            PortfolioData(
                portfolio_name=row["portfolio_name"],
                portfolio_id=row["portfolio_id"],
                avatar=row["avatar"],
                total_value=row["total_value"],
                value_change_24h=row["value_change_24h"],
                percent_change_24h=row["percent_change_24h"],
            )
            for row in rows
        ]

    async def _prepare_data(self, data: Sequence[PortfolioData]) -> list[PortfolioData]:
        result: list[PortfolioData] = []

        for portfolio in data:
            avatar = portfolio["avatar"]
            portfolio_id = portfolio["portfolio_id"]

            if portfolio["portfolio_name"] == "All Portfolios":
                avatar = None
                portfolio_id = None
            elif avatar is not None:
                avatar = await self._minio.get_presigned_url(avatar)

            new_portfolio: PortfolioData = {
                "portfolio_name": portfolio["portfolio_name"],
                "portfolio_id": portfolio_id,
                "avatar": avatar,
                "total_value": portfolio["total_value"],
                "value_change_24h": portfolio["value_change_24h"],
                "percent_change_24h": portfolio["percent_change_24h"],
            }

            result.append(new_portfolio)

        return result

    async def get_portfolios_with_presigned_urls(
        self, user_id: int
    ) -> list[PortfolioData]:
        portfolios_data = await self._get_portfolios(user_id)
        return await self._prepare_data(portfolios_data)

    async def get_portfolio_transactions(
        self, portfolio_id: int, user_id: int, limit: int = 20, offset: int = 0
    ) -> list[TransactionData]:
        stmt = (
            select(
                transactions_table.c.transaction_id.label("transaction_id"),
                transactions_table.c.transaction_type.label("transaction_type"),
                transactions_table.c.created_at.label("transaction_time"),
                transactions_table.c.quantity.label("quantity"),
                assets_table.c.asset_id.label("asset_id"),
                assets_table.c.symbol.label("asset_symbol"),
                assets_table.c.name.label("asset_name"),
                transactions_table.c.price.label("purchase_price"),
                assets_table.c.price_usd.label("current_price"),
                transactions_table.c.note.label("note"),
            )
            .select_from(
                transactions_table.join(
                    assets_table,
                    transactions_table.c.asset_id == assets_table.c.asset_id,
                ).join(
                    portfolios_table,
                    transactions_table.c.portfolio_id
                    == portfolios_table.c.portfolio_id,
                )
            )
            .where(
                transactions_table.c.portfolio_id == portfolio_id,
                portfolios_table.c.user_id == user_id,
            )
            .limit(limit)
            .offset(offset)
        )

        result = await self._session.execute(stmt)
        rows = result.mappings().all()

        transactions: list[TransactionData] = []

        for row in rows:
            transactions.append(
                TransactionData(
                    transaction_id=row["transaction_id"],
                    transaction_type=row["transaction_type"],
                    transaction_time=row["transaction_time"].isoformat(),
                    quantity=row["quantity"],
                    asset_id=row["asset_id"],
                    asset_symbol=row["asset_symbol"],
                    asset_name=row["asset_name"],
                    purchase_price=row["purchase_price"],
                    current_price=row["current_price"],
                    note=row["note"],
                )
            )

        return transactions
