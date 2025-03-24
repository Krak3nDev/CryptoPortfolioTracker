from cryptoapp.domain.entities.portfolio.gateway import PortfolioGateway
from cryptoapp.domain.entities.portfolio.portfolio import Portfolio, PortfolioId
from cryptoapp.domain.entities.user.user import UserId


class PortfolioFactory:
    def __init__(self, gateway: PortfolioGateway):
        self._gateway = gateway

    async def create(
        self, name: str, avatar: str, identity: int | None, user_id: int
    ) -> Portfolio:
        portfolio = Portfolio(
            _identity=PortfolioId(identity),
            _name=name,
            _avatar=avatar,
            _transactions=[],
            _user_id=UserId(user_id),
        )

        self._gateway.add(portfolio=portfolio)

        return portfolio
