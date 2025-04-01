from dataclasses import dataclass

from cryptoapp.application.common.id_provider import IdProvider
from cryptoapp.application.common.transaction_manager import TransactionManager
from cryptoapp.domain.entities.portfolio.gateway import PortfolioGateway
from cryptoapp.domain.entities.portfolio.portfolio import PortfolioId
from cryptoapp.domain.entities.user.user import UserId
from cryptoapp.domain.exceptions import EntityNotFound


@dataclass
class DeletePortfolioRequest:
    portfolio_id: int


class DeletePortfolio:
    def __init__(
        self,
        portfolio_gateway: PortfolioGateway,
        transaction_manager: TransactionManager,
        id_provider: IdProvider,
    ):
        self._portfolio_gateway = portfolio_gateway
        self._tr_manager = transaction_manager
        self._id_provider = id_provider

    async def __call__(self, data: DeletePortfolioRequest) -> None:
        user_id = await self._id_provider.get_current_user_id()

        portfolio = await self._portfolio_gateway.by_identity(
            portfolio_id=PortfolioId(data.portfolio_id), user_id=UserId(user_id)
        )

        if not portfolio:
            raise EntityNotFound(field_name="Portfolio", value=data.portfolio_id)

        await self._portfolio_gateway.delete(portfolio=portfolio)

        await self._tr_manager.commit()
