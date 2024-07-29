from cryptoapp.application.interfaces.uow import UoW
from sqlalchemy.ext.asyncio import AsyncSession


class SQLAlchemyUoW(UoW):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def commit(self) -> None:
        await self.session.commit()

    async def flush(self) -> None:
        await self.session.flush()

    async def rollback(self) -> None:
        await self.session.rollback()
