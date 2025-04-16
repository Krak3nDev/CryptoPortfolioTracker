from dataclasses import dataclass

from cryptoapp.application.common.id_provider import IdProvider
from cryptoapp.application.common.transaction_manager import TransactionManager
from cryptoapp.application.portfolio.shared import (
    get_portfolio_with_ownership_check,
)
from cryptoapp.domain.entities.portfolio.repository import PortfolioRepository


@dataclass
class DeletePortfolioRequest:
    portfolio_id: int


class DeletePortfolio:
    def __init__(
        self,
        portfolio_repository: PortfolioRepository,
        transaction_manager: TransactionManager,
        id_provider: IdProvider,
    ):
        self._portfolio_repository = portfolio_repository
        self._tr_manager = transaction_manager
        self._id_provider = id_provider

    async def __call__(self, data: DeletePortfolioRequest) -> None:
        user_id = await self._id_provider.get_current_user_id()

        portfolio = await get_portfolio_with_ownership_check(
            portfolio_repository=self._portfolio_repository,
            user_id=user_id,
            portfolio_id=data.portfolio_id,
        )

        await self._portfolio_repository.delete(portfolio=portfolio)

        await self._tr_manager.commit()
