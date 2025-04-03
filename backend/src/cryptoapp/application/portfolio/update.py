from dataclasses import dataclass

from cryptoapp.application.common.id_provider import IdProvider
from cryptoapp.application.common.transaction_manager import TransactionManager
from cryptoapp.application.interfaces.storage import StorageService
from cryptoapp.domain.entities.portfolio.portfolio import PortfolioId
from cryptoapp.domain.entities.portfolio.repository import PortfolioRepository
from cryptoapp.domain.entities.user.user import UserId
from cryptoapp.domain.exceptions import EntityNotFound


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

        portfolio = await self._portfolio_repository.by_identity(
            portfolio_id=PortfolioId(data.portfolio_id),
            user_id=UserId(user_id),
        )

        if not portfolio:
            raise EntityNotFound(
                field_name="Portfolio", value=data.portfolio_id
            )

        if data.avatar:
            avatar_url = await self._storage.upload_from_bytes(
                data=data.avatar, file_name=f"avatar_{user_id}"
            )
            portfolio.avatar = avatar_url

        if data.name:
            portfolio.name = data.name

        await self._tr_manager.commit()
