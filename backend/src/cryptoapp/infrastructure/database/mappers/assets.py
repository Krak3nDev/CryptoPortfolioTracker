import logging
from datetime import datetime, timezone
from typing import Sequence, Any

from sqlalchemy import select, RowMapping, update, Row
from sqlalchemy.dialects.postgresql import insert

from cryptoapp.domain.entities.asset import Asset
from cryptoapp.infrastructure.database.mappers.base import SessionInitializer
from cryptoapp.infrastructure.database.models.assets import AssetDB
from cryptoapp.infrastructure.services.api.structures import CryptoData, DBAssetDict


def extract_asset_data(asset: CryptoData) -> DBAssetDict:
    usd_data = asset["quote"]["USD"]
    return DBAssetDict(
        crypto_id=asset["id"],
        name=asset["name"],
        symbol=asset["symbol"],
        slug=asset["slug"],
        cmc_rank=asset["cmc_rank"],
        price=usd_data["price"],
        percent_change_1h=usd_data["percent_change_1h"],
        percent_change_24h=usd_data["percent_change_24h"],
        percent_change_7d=usd_data["percent_change_7d"],
        last_updated=datetime.fromisoformat(usd_data["last_updated"].replace("Z", "+00:00")).astimezone(timezone.utc),
    )


def collect_assets_to_update(
    new_assets: Sequence[CryptoData],
    existing_assets: Sequence[RowMapping]) -> list[DBAssetDict]:
    existing_assets_dict = {asset['crypto_id']: asset for asset in existing_assets}
    assets_to_update = []

    for asset in new_assets:
        current_asset_id = asset["id"]
        extracted_data = extract_asset_data(asset)
        logging.error(
            type(extracted_data["last_updated"])
        )
        new_last_updated = extracted_data["last_updated"]

        if current_asset_id not in existing_assets_dict:
            logging.debug(f"Adding new asset: {extracted_data}")
            assets_to_update.append(extracted_data)
        else:
            old_asset = existing_assets_dict[current_asset_id]
            old_last_updated = old_asset["last_updated"]
            logging.debug(f"Comparing assets: new {new_last_updated} vs old {old_last_updated}")

            if new_last_updated > old_last_updated:
                logging.debug(f"Updating asset: {extracted_data}")
                assets_to_update.append(extracted_data)

    return assets_to_update


class AssetMapper(SessionInitializer):
    def _load(self, row: Row[Any]) -> Asset:
        return Asset(
            id=row.crypto_id,
            name=row.name,
            symbol=row.symbol,
            slug=row.slug,
            price=row.price,
            percent_change_1h=row.percent_change_1h,
            percent_change_24h=row.percent_change_24h,
            percent_change_7d=row.percent_change_7d,
        )

    async def get_assets(self) -> Sequence[RowMapping]:
        statement = select(AssetDB.crypto_id, AssetDB.last_updated)
        result = await self.session.execute(statement)
        return result.mappings().all()

    async def bulk_update(self, assets_to_update: list[dict[str, Any]]) -> None:
        statement = update(AssetDB)
        await self.session.execute(
            statement,
            assets_to_update
        )
 
    async def bulk_upsert(self, assets: list[DBAssetDict]) -> None:
        statement = insert(AssetDB)
        do_update_stmt = statement.on_conflict_do_update(
            index_elements=[AssetDB.crypto_id],
            set_=dict(
                price=statement.excluded.price,
                last_updated=statement.excluded.last_updated,
                percent_change_1h=statement.excluded.percent_change_1h,
                percent_change_24h=statement.excluded.percent_change_24h,
                percent_change_7d=statement.excluded.percent_change_7d,
            )
        )
        await self.session.execute(do_update_stmt, assets)
