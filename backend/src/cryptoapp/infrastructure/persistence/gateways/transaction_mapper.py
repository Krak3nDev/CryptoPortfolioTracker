from sqlalchemy import select

from cryptoapp.domain.entities.transaction.gateway import TransactionGateway
from cryptoapp.infrastructure.persistence.gateways.base import SessionInitializer
from cryptoapp.infrastructure.persistence.tables import assets_table


class TransactionMapper(SessionInitializer, TransactionGateway):
    async def asset_exist(self, asset_id: int) -> bool:
        stmt = select(assets_table).where(assets_table.c.asset_id == asset_id)
        return bool(await self._session.scalar(stmt))
