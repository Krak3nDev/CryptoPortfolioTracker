from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from cryptoapp.infrastructure.database.mappers.assets import AssetMapper, collect_assets_to_update
from cryptoapp.infrastructure.services.api.coin_market import CoinMarketApi
from cryptoapp.main.depedencies.ioc_container import container


def start_scheduler() -> None:
    scheduler = AsyncIOScheduler()
    scheduler.add_job(update_assets, IntervalTrigger(minutes=3))
    scheduler.start()
    

async def update_assets() -> None:
    async with container() as c:
        coin_market_api: CoinMarketApi = await c.get(CoinMarketApi)
        asset_mapper: AssetMapper = await c.get(AssetMapper)

        async with coin_market_api:
            _, response = await coin_market_api.get_assets()
            new_assets = response["data"]

        existing_assets = await asset_mapper.get_assets()
        assets_to_update = collect_assets_to_update(
            new_assets=new_assets, existing_assets=existing_assets
        )

        if assets_to_update:
            await asset_mapper.bulk_upsert(assets_to_update)
            await asset_mapper.session.commit()
