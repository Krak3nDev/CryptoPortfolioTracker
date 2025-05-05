from itertools import batched
from typing import Iterable

from sqlalchemy import delete
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from cryptoapp.infrastructure.persistence.tables import (
    assets_table,
    assets_tags_table,
    tags_table,
)
from cryptoapp.infrastructure.services.assets_updater.schemas import AssetRow
from cryptoapp.infrastructure.services.assets_updater.utils import (
    build_assets_tags_rows,
    extract_tags,
    prepare_asset_rows,
)
from cryptoapp.infrastructure.services.marcetcap_api.api import (
    CoinMarketCapAPI,
    retrieve_all_data,
)


async def upsert_assets(
    data: Iterable[AssetRow], session: AsyncSession
) -> None:
    insert_stmt = insert(assets_table).values(
        [
            {
                "cmc_id": row["cmc_id"],
                "name": row["name"],
                "symbol": row["symbol"],
                "slug": row["slug"],
                "date_added": row["date_added"],
                "is_infinite_supply": row["is_infinite_supply"],
                "max_supply": row["max_supply"],
                "total_supply": row["total_supply"],
                "circulating_supply": row["circulating_supply"],
                "price_usd": row["price_usd"],
                "volume_24h_usd": row["volume_24h_usd"],
                "market_cap_usd": row["market_cap_usd"],
                "percent_change_1h_usd": row["percent_change_1h_usd"],
                "percent_change_24h_usd": row["percent_change_24h_usd"],
                "percent_change_7d_usd": row["percent_change_7d_usd"],
                "last_updated": row["last_updated"],
            }
            for row in data
        ]
    )
    insert_stmt = insert_stmt.on_conflict_do_update(  # type: ignore
        index_elements=[assets_table.c.cmc_id],
        set_={
            "cmc_id": insert_stmt.excluded.cmc_id,
            "name": insert_stmt.excluded.name,
            "symbol": insert_stmt.excluded.symbol,
            "slug": insert_stmt.excluded.slug,
            "date_added": insert_stmt.excluded.date_added,
            "is_infinite_supply": insert_stmt.excluded.is_infinite_supply,
            "max_supply": insert_stmt.excluded.max_supply,
            "total_supply": insert_stmt.excluded.total_supply,
            "circulating_supply": insert_stmt.excluded.circulating_supply,
            "price_usd": insert_stmt.excluded.price_usd,
            "volume_24h_usd": insert_stmt.excluded.volume_24h_usd,
            "market_cap_usd": insert_stmt.excluded.market_cap_usd,
            "percent_change_1h_usd": insert_stmt.excluded.percent_change_1h_usd,  # noqa: E501
            "percent_change_24h_usd": insert_stmt.excluded.percent_change_24h_usd,  # noqa: E501
            "percent_change_7d_usd": insert_stmt.excluded.percent_change_7d_usd,  # noqa: E501
            "last_updated": insert_stmt.excluded.last_updated,
        },
        where=(
            insert_stmt.excluded.last_updated > assets_table.c.last_updated
        ),
    ).returning(assets_table.c.asset_id, assets_table.c.cmc_id)

    result_assets = await session.execute(insert_stmt)
    rows_assets = result_assets.fetchall()

    asset_id_map = {
        returned_cmc_id: returned_asset_id
        for returned_asset_id, returned_cmc_id in rows_assets
    }

    if asset_id_map:
        stmt_delete = delete(assets_tags_table).where(
            assets_tags_table.c.asset_id.in_(asset_id_map.values())
        )
        await session.execute(stmt_delete)

    cmc_id_to_tag_names, all_tag_names = extract_tags(data, asset_id_map)
    tag_rows = [{"name": tag_name} for tag_name in all_tag_names]

    if tag_rows:
        stmt_tags = (
            insert(tags_table)
            .values(tag_rows)
            .on_conflict_do_update(
                index_elements=[tags_table.c.name],
                set_={"name": insert(tags_table).excluded.name},
            )
            .returning(tags_table.c.tag_id, tags_table.c.name)
        )
        result_tags = await session.execute(stmt_tags)
        rows_tags = result_tags.fetchall()
    else:
        rows_tags = []

    tag_id_map = {name: tag_id for (tag_id, name) in rows_tags}

    assets_tags_rows = build_assets_tags_rows(
        cmc_id_to_tag_names=cmc_id_to_tag_names,
        asset_id_map=asset_id_map,
        tag_id_map=tag_id_map,
    )

    if assets_tags_rows:
        stmt_assets_tags = (
            insert(assets_tags_table)
            .values(assets_tags_rows)
            .on_conflict_do_nothing(
                index_elements=[
                    assets_tags_table.c.asset_id,
                    assets_tags_table.c.tag_id,
                ]
            )
        )
        await session.execute(stmt_assets_tags)
    await session.commit()


async def update_all_assets(
    api: CoinMarketCapAPI,
    session: AsyncSession,
) -> None:
    raw_data = await retrieve_all_data(api)
    assets = prepare_asset_rows(raw_data)
    for chunk in batched(assets, 2000):
        await upsert_assets(data=chunk, session=session)
