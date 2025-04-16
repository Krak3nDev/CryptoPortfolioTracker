from dataclasses import dataclass

from cryptoapp.domain.entities.identity import Identity
from cryptoapp.domain.entities.user.user import UserId


class PortfolioId(Identity):
    pass


@dataclass
class Portfolio:
    _identity: PortfolioId
    _user_id: UserId
    _name: str
    _avatar: str

    @classmethod
    def create(
        cls,
        portfolio_id: int | None,
        user_id: int,
        name: str,
        avatar: str,
    ) -> "Portfolio":
        return cls(
            _identity=PortfolioId(portfolio_id),
            _user_id=UserId(user_id),
            _name=name,
            _avatar=avatar,
        )

    @property
    def identity(self) -> PortfolioId:
        return self._identity

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def avatar(self) -> str:
        return self._avatar

    @avatar.setter
    def avatar(self, value: str) -> None:
        self._avatar = value
