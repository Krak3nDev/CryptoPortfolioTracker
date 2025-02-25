from sqlalchemy.ext.asyncio import AsyncSession

from cryptoapp.application.common.transaction_manager import TransactionManager


class AlchemyTransactionManager(TransactionManager):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def commit(self) -> None:
        await self.session.commit()

    async def flush(self) -> None:
        await self.session.flush()

    async def rollback(self) -> None:
        await self.session.rollback()
