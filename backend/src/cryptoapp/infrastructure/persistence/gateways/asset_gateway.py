from sqlalchemy import select

from cryptoapp.application.interfaces.asset_gateway import AssetGateway
from cryptoapp.infrastructure.persistence.gateways.base import (
    SessionInitializer,
)
from cryptoapp.infrastructure.persistence.tables import assets_table


class AssetMapper(SessionInitializer, AssetGateway):
    async def asset_exist(self, asset_id: int) -> bool:
        stmt = select(assets_table).where(assets_table.c.asset_id == asset_id)
        return bool(await self._session.scalar(stmt))
