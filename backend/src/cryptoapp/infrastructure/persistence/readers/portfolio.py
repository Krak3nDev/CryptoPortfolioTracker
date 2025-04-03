from decimal import Decimal
from typing import Sequence, TypedDict

from sqlalchemy import case, func, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from cryptoapp.domain.entities.transaction.transaction import TransactionType
from cryptoapp.infrastructure.persistence.gateways.base import (
    SessionInitializer,
)
from cryptoapp.infrastructure.persistence.tables import (
    assets_table,
    portfolios_table,
    transactions_table,
)
from cryptoapp.infrastructure.services.minio import S3Minio


class PortfolioData(TypedDict):
    portfolio_name: str
    portfolio_id: int
    avatar: str
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


class TransactionsPage(TypedDict):
    next_cursor: int | None
    items: list[TransactionData]


class Asset(TypedDict):
    asset_id: int
    asset_symbol: str
    total_quantity: Decimal
    current_price: Decimal
    change_1h: Decimal
    change_24h: Decimal
    change_7d: Decimal
    total_value: Decimal
    allocation_percentage: Decimal


class PortfolioSummary(TypedDict):
    total_value: Decimal | None
    total_value_change_24h: Decimal | None
    total_value_change_24h_percentage: Decimal | None
    holdings: list[Asset]


class PerformerData(TypedDict):
    symbol: str
    name: str
    change_value: Decimal
    change_percentage: Decimal


class AssetWithProfitLoss(TypedDict):
    asset_id: int
    asset_symbol: str
    asset_name: str
    total_quantity: Decimal
    average_buy_price: Decimal
    current_price: Decimal
    change_1h: Decimal
    change_24h: Decimal
    change_7d: Decimal
    total_value: Decimal
    profit_loss_usd: Decimal
    profit_loss_percentage: Decimal
    allocation_percentage: Decimal


class PortfolioStats(TypedDict):
    total_value: Decimal | None
    total_value_change_24h: Decimal | None
    total_value_change_24h_percentage: Decimal | None
    all_time_profit: Decimal | None
    cost_basis: Decimal | None
    best_performer: PerformerData | None
    worst_performer: PerformerData | None
    holdings: list[AssetWithProfitLoss]


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
                            transactions_table.c.transaction_type
                            == "transfer_in",
                            transactions_table.c.quantity,
                        ),
                        (
                            transactions_table.c.transaction_type
                            == "transfer_out",
                            -transactions_table.c.quantity,
                        ),
                        else_=0,
                    )
                ).label("total_quantity"),
                assets_table.c.price_usd.label("current_price"),
                (
                    assets_table.c.price_usd
                    * func.sum(transactions_table.c.quantity)
                ).label("current_value"),
                (
                    assets_table.c.price_usd
                    * func.sum(transactions_table.c.quantity)
                    * assets_table.c.percent_change_24h_usd
                    / 100
                ).label("value_change_24h"),
                assets_table.c.percent_change_24h_usd.label(
                    "percent_change_24h"
                ),
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
                func.sum(portfolio_assets.c.current_value).label(
                    "total_value"
                ),
                func.sum(portfolio_assets.c.value_change_24h).label(
                    "value_change_24h"
                ),
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

        portfolios_with_values = (
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
            )
            .select_from(
                user_portfolios.outerjoin(
                    portfolio_totals_with_transactions,
                    user_portfolios.c.portfolio_id
                    == portfolio_totals_with_transactions.c.portfolio_id,
                )
            )
            .order_by(user_portfolios.c.portfolio_id)
        )

        result = await self._session.execute(portfolios_with_values)
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

    async def _prepare_data(
        self, data: Sequence[PortfolioData]
    ) -> list[PortfolioData]:
        result: list[PortfolioData] = []

        for portfolio in data:
            avatar = portfolio["avatar"]
            portfolio_id = portfolio["portfolio_id"]

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
        self,
        portfolio_id: int,
        user_id: int,
        limit: int = 20,
        last_transaction_id: int | None = None,
    ) -> TransactionsPage:
        transaction_id_condition = (
            "AND t.transaction_id > :last_transaction_id"
            if last_transaction_id is not None
            else ""
        )

        sql = text(f"""
        WITH base AS (
            SELECT
                t.transaction_id,
                t.transaction_type,
                t.created_at,
                t.quantity,
                a.asset_id,
                a.symbol  AS asset_symbol,
                a.name    AS asset_name,
                t.price   AS purchase_price,
                a.price_usd AS current_price,
                t.note
            FROM transactions t
            JOIN assets a
                ON t.asset_id = a.asset_id
            JOIN portfolios p
                ON t.portfolio_id = p.portfolio_id
            WHERE t.portfolio_id = :portfolio_id 
                AND p.user_id = :user_id
                {transaction_id_condition}
            ORDER BY t.transaction_id ASC
            LIMIT :limit
        )
        SELECT json_build_object(
            'next_cursor',
            (
              SELECT transaction_id
              FROM base
              ORDER BY transaction_id DESC
              LIMIT 1
            ),
            'items',
            COALESCE(
                json_agg(
                   json_build_object(
                      'transaction_id', base.transaction_id,
                        'transaction_type', base.transaction_type,
                        'transaction_time',
                            to_char(
                                base.created_at,
                                'YYYY-MM-DD"T"HH24:MI:SSOF'
                            ),
                        'quantity', base.quantity,
                        'asset_id', base.asset_id,
                        'asset_symbol', base.asset_symbol,
                        'asset_name', base.asset_name,
                        'purchase_price', base.purchase_price,
                        'current_price', base.current_price,
                        'note', base.note
                   )
                   ORDER BY base.transaction_id
                ),
                '[]'::json
            )
        )::text AS result_json
        FROM base
        ;
        """)

        params = {
            "portfolio_id": portfolio_id,
            "user_id": user_id,
            "limit": limit,
        }

        if last_transaction_id is not None:
            params["last_transaction_id"] = last_transaction_id

        result: TransactionsPage = await self._session.scalar(sql, params)

        return result

    async def get_portfolio_stats(self, user_id: int) -> PortfolioSummary:
        sql = text("""
        WITH holdings AS (
            SELECT
                a.asset_id,
                a.symbol AS asset_symbol,
                SUM(
                    CASE
                        WHEN t.transaction_type IN ('buy', 'transfer_in')
                        THEN t.quantity
                        WHEN t.transaction_type IN ('sell', 'transfer_out')
                        THEN -t.quantity
                        ELSE 0
                    END
                ) AS total_quantity,
                a.price_usd             AS current_price,
                a.percent_change_1h_usd AS change_1h,
                a.percent_change_24h_usd AS change_24h,
                a.percent_change_7d_usd  AS change_7d
            FROM portfolios p
            JOIN transactions t
              ON p.portfolio_id = t.portfolio_id
            JOIN assets a
              ON t.asset_id = a.asset_id
            WHERE p.user_id = :user_id
            GROUP BY
                a.asset_id,
                a.symbol,
                a.price_usd,
                a.percent_change_1h_usd,
                a.percent_change_24h_usd,
                a.percent_change_7d_usd
        ),
        final_data AS (
            SELECT
                SUM(h.total_quantity * h.current_price) OVER ()
                    AS portfolio_value,
                SUM(
                    h.total_quantity * h.current_price * h.change_24h / 100
                ) OVER () AS total_value_change_24h,
                (
                    SUM(
                        h.total_quantity * h.current_price * h.change_24h / 100
                    ) OVER ()
                    / NULLIF(
                        SUM(h.total_quantity * h.current_price) OVER (),
                        0
                    )
                    * 100
                ) AS total_value_change_24h_percentage,
                h.asset_id,
                h.asset_symbol,
                h.total_quantity,
                h.current_price,
                h.change_1h,
                h.change_24h,
                h.change_7d,
                (h.total_quantity * h.current_price) AS holding_value,
                (
                    (h.total_quantity * h.current_price)
                    / NULLIF(
                        SUM(h.total_quantity * h.current_price) OVER (),
                        0
                    )
                    * 100
                ) AS allocation_percentage
            FROM holdings h
        )
        SELECT
            json_build_object(
                'portfolio_value',
                MAX(fd.portfolio_value),
                'total_value_change_24h',
                MAX(fd.total_value_change_24h),
                'total_value_change_24h_percentage',
                MAX(fd.total_value_change_24h_percentage),
                'holdings',
                json_agg(
                    json_build_object(
                        'asset_id', fd.asset_id,
                        'asset_symbol', fd.asset_symbol,
                        'total_quantity', fd.total_quantity,
                        'current_price', fd.current_price,
                        'change_1h', fd.change_1h,
                        'change_24h', fd.change_24h,
                        'change_7d', fd.change_7d,
                        'holding_value', fd.holding_value,
                        'allocation_percentage', fd.allocation_percentage
                    )
                    ORDER BY fd.holding_value DESC
                )
            ) AS portfolio_json
        FROM final_data fd
        ;
        """)

        result: PortfolioSummary = await self._session.scalar(
            sql, {"user_id": user_id}
        )

        return result

    async def get_portfolio_stats_by_portfolio_id(
        self, portfolio_id: int, user_id: int
    ) -> PortfolioStats:
        sql = text("""
        WITH portfolio_check AS (
            SELECT portfolio_id
            FROM portfolios
            WHERE portfolio_id = :portfolio_id
              AND user_id = :user_id
        ),

        holdings AS (
            SELECT
                a.asset_id,
                a.symbol AS asset_symbol,
                a.name AS asset_name,
                SUM(
                    CASE
                        WHEN t.transaction_type IN ('buy', 'transfer_in')
                        THEN t.quantity
                        WHEN t.transaction_type IN ('sell', 'transfer_out')
                        THEN -t.quantity
                        ELSE 0
                    END
                ) AS total_quantity,
                SUM(
                    CASE
                        WHEN t.transaction_type IN ('buy', 'transfer_in')
                        THEN t.quantity * t.price
                        ELSE 0
                    END
                ) AS total_spent,
                SUM(
                    CASE
                        WHEN t.transaction_type IN ('sell', 'transfer_out')
                        THEN t.quantity * t.price
                        ELSE 0
                    END
                ) AS total_sold,
                a.price_usd AS current_price,
                a.percent_change_1h_usd AS change_1h,
                a.percent_change_24h_usd AS change_24h,
                a.percent_change_7d_usd AS change_7d
            FROM transactions t
            JOIN assets a ON t.asset_id = a.asset_id
            JOIN portfolios p ON t.portfolio_id = p.portfolio_id
            WHERE t.portfolio_id = :portfolio_id
              AND p.user_id = :user_id
            GROUP BY
                a.asset_id,
                a.symbol,
                a.name,
                a.price_usd,
                a.percent_change_1h_usd,
                a.percent_change_24h_usd,
                a.percent_change_7d_usd
        ),

        holdings_with_derived AS (
            SELECT
                h.*,
                (h.total_quantity * h.current_price) AS holding_value,
                CASE WHEN h.total_quantity > 0
                    THEN (h.total_spent / h.total_quantity)
                    ELSE 0
                END AS average_buy_price,
                (
                    h.total_quantity * h.current_price
                    - h.total_spent
                ) AS profit_loss_usd,
                CASE WHEN h.total_spent > 0
                    THEN (
                        (h.total_quantity * h.current_price - h.total_spent)
                        / h.total_spent
                        * 100
                    )
                    ELSE 0
                END AS profit_loss_percentage,
                (
                    (h.change_24h / 100) * h.total_quantity * h.current_price
                ) AS change_value_24h
            FROM holdings h
            WHERE h.total_quantity > 0
        ),

        aggregated_data AS (
            SELECT
                SUM(h.holding_value) AS total_value,
                SUM(h.change_value_24h) AS total_value_change_24h,
                SUM(h.total_spent) AS cost_basis,
                (
                    SUM(h.holding_value)
                    - SUM(h.total_spent)
                    + SUM(h.total_sold)
                ) AS all_time_profit,
                CASE WHEN SUM(h.holding_value) > 0
                    THEN (
                        SUM(h.change_value_24h)
                        / SUM(h.holding_value)
                        * 100
                    )
                    ELSE 0
                END AS total_value_change_24h_percentage
            FROM holdings_with_derived h
        ),

        best_performer AS (
            SELECT
                h.asset_symbol AS symbol,
                h.asset_name AS name,
                h.change_value_24h AS change_value,
                h.change_24h AS change_percentage
            FROM holdings_with_derived h
            WHERE h.holding_value >= 10
            ORDER BY h.change_24h DESC
            LIMIT 1
        ),

        worst_performer AS (
            SELECT
                h.asset_symbol AS symbol,
                h.asset_name AS name,
                h.change_value_24h AS change_value,
                h.change_24h AS change_percentage
            FROM holdings_with_derived h
            WHERE h.holding_value >= 10
            ORDER BY h.change_24h ASC
            LIMIT 1
        ),

        final_holdings AS (
            SELECT
                h.asset_id,
                h.asset_symbol,
                h.asset_name,
                h.total_quantity,
                h.average_buy_price,
                h.current_price,
                h.change_1h,
                h.change_24h,
                h.change_7d,
                h.holding_value AS total_value,
                h.profit_loss_usd,
                h.profit_loss_percentage,
                CASE WHEN (SELECT total_value FROM aggregated_data) > 0
                    THEN (
                        h.holding_value
                        / (SELECT total_value FROM aggregated_data)
                        * 100
                    )
                    ELSE 0
                END AS allocation_percentage
            FROM holdings_with_derived h
        )

        SELECT json_build_object(
        'total_value',
            (SELECT total_value FROM aggregated_data),
        'total_value_change_24h',
            (SELECT total_value_change_24h FROM aggregated_data),
        'total_value_change_24h_percentage',
            (SELECT total_value_change_24h_percentage FROM aggregated_data),
        'cost_basis',
            (SELECT cost_basis FROM aggregated_data),
        'all_time_profit',
            COALESCE((SELECT all_time_profit FROM aggregated_data), 0),
        'best_performer',
                CASE WHEN (SELECT COUNT(*) FROM best_performer) > 0
                THEN (
                    SELECT json_build_object(
                        'symbol', symbol,
                        'name', name,
                        'change_value', change_value,
                        'change_percentage', change_percentage
                    )
                    FROM best_performer
                )
                ELSE NULL
                END,
        'worst_performer',
                CASE WHEN (SELECT COUNT(*) FROM worst_performer) > 0
                THEN (
                    SELECT json_build_object(
                        'symbol', symbol,
                        'name', name,
                        'change_value', change_value,
                        'change_percentage', change_percentage
                    )
                    FROM worst_performer
                )
                ELSE NULL
                END,
        'holdings',
            COALESCE(
                (
                    SELECT json_agg(
                        json_build_object(
                            'asset_id', asset_id,
                            'asset_symbol', asset_symbol,
                            'asset_name', asset_name,
                            'total_quantity', total_quantity,
                            'average_buy_price', average_buy_price,
                            'current_price', current_price,
                            'change_1h', change_1h,
                            'change_24h', change_24h,
                            'change_7d', change_7d,
                            'total_value', total_value,
                            'profit_loss_usd', profit_loss_usd,
                            'profit_loss_percentage', profit_loss_percentage,
                            'allocation_percentage', allocation_percentage
                        )
                        ORDER BY total_value DESC
                    )
                    FROM final_holdings
                ),
                '[]'::json
            )
        ) AS portfolio_stats_json
        FROM (
            SELECT 1
            WHERE EXISTS (SELECT 1 FROM portfolio_check)
        ) dummy
        UNION ALL
        SELECT json_build_object(
            'total_value', NULL,
            'total_value_change_24h', NULL,
            'total_value_change_24h_percentage', NULL,
            'cost_basis', NULL,
            'all_time_profit', NULL,
            'best_performer', NULL,
            'worst_performer', NULL,
            'holdings', '[]'::json
        ) AS portfolio_stats_json
        WHERE NOT EXISTS (SELECT 1 FROM portfolio_check)
            OR NOT EXISTS (SELECT 1 FROM holdings_with_derived)
        LIMIT 1
        """)

        result: PortfolioStats = await self._session.scalar(
            sql, {"portfolio_id": portfolio_id, "user_id": user_id}
        )
        return result
