from dataclasses import dataclass

from cryptoapp.application.common.id_provider import IdProvider
from cryptoapp.application.common.transaction_manager import TransactionManager
from cryptoapp.application.interfaces.storage import StorageService
from cryptoapp.application.portfolio.shared import (
    get_portfolio_with_ownership_check,
)
from cryptoapp.domain.entities.portfolio.repository import PortfolioRepository


@dataclass
class UpdatePortfolioRequest:
    portfolio_id: int
    avatar: bytes | None
    name: str | None


class UpdatePortfolio:
    def __init__(
        self,
        portfolio_repository: PortfolioRepository,
        id_provider: IdProvider,
        tr_manager: TransactionManager,
        storage: StorageService,
    ) -> None:
        self._portfolio_repository = portfolio_repository
        self._id_provider = id_provider
        self._tr_manager = tr_manager
        self._storage = storage

    async def __call__(self, data: UpdatePortfolioRequest) -> None:
        user_id = await self._id_provider.get_current_user_id()

        portfolio = await get_portfolio_with_ownership_check(
            portfolio_repository=self._portfolio_repository,
            user_id=user_id,
            portfolio_id=data.portfolio_id,
        )

        if data.avatar:
            avatar_url = await self._storage.upload_from_bytes(
                data=data.avatar, file_name=f"avatar_{user_id}"
            )
            portfolio.avatar = avatar_url

        if data.name:
            portfolio.name = data.name

        await self._tr_manager.commit()
