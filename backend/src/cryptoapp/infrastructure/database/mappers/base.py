from sqlalchemy.ext.asyncio import AsyncSession


class SessionInitializer:
    def __init__(self, session: AsyncSession):
        self.session = session
