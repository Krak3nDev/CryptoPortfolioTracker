from dataclasses import dataclass
from datetime import datetime, timezone

from cryptoapp.application.common.id_provider import IdProvider
from cryptoapp.application.common.transaction_manager import TransactionManager
from cryptoapp.application.common.validators import validate_length
from cryptoapp.application.interfaces.storage import StorageService
from cryptoapp.domain.entities.portfolio.gateway import PortfolioGateway
from cryptoapp.domain.entities.portfolio.portfolio import Portfolio


@dataclass
class CreationPortfolioRequest:
    name: str
    avatar: bytes | None


@dataclass
class CreationPortfolioResponse:
    portfolio_id: int
    name: str
    avatar: str
    created_at: str


BUCKET = "my-portfolios-bucket"


class CreatePortfolio:
    def __init__(
        self,
        portfolio_gateway: PortfolioGateway,
        tr_manager: TransactionManager,
        storage: StorageService,
        identity_provider: IdProvider,
    ) -> None:
        self._portfolio_gateway = portfolio_gateway
        self._tr_manager = tr_manager
        self._storage = storage
        self._identity_provider = identity_provider

    async def __call__(
        self, data: CreationPortfolioRequest
    ) -> CreationPortfolioResponse:
        validate_length(max_length=50, field_name="name", value=data.name)

        user_id = await self._identity_provider.get_current_user_id()

        if data.avatar:
            avatar_url = await self._storage.upload_from_bytes(
                data=data.avatar, file_name=f"avatar_{user_id}"
            )
        else:
            avatar_url = f"s3://{BUCKET}/defaults/default_avatar.webp"

        portfolio = Portfolio.create(
            name=data.name, avatar=avatar_url, portfolio_id=None, user_id=user_id
        )

        self._portfolio_gateway.add(portfolio)

        await self._tr_manager.commit()

        return CreationPortfolioResponse(
            portfolio_id=portfolio.identity.value,
            name=portfolio.name,
            avatar=portfolio.avatar,
            created_at=datetime.now(timezone.utc).isoformat(),
        )
