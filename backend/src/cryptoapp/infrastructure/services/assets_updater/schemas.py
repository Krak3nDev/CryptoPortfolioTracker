from datetime import datetime
from decimal import Decimal
from typing import NamedTuple, TypeAlias, TypedDict

CmcIdToTagNames: TypeAlias = dict[int, list[str]]


class AssetRow(TypedDict):
    cmc_id: int
    name: str
    symbol: str
    slug: str
    date_added: datetime
    is_infinite_supply: bool
    tags: list[str]
    max_supply: Decimal | None
    total_supply: Decimal
    circulating_supply: Decimal
    price_usd: Decimal
    volume_24h_usd: Decimal
    market_cap_usd: Decimal
    percent_change_1h_usd: Decimal
    percent_change_24h_usd: Decimal
    percent_change_7d_usd: Decimal
    last_updated: datetime


class AssetTagLink(TypedDict):
    asset_id: int
    tag_id: int


class TagExtractionResult(NamedTuple):
    cmc_id_to_tag_names: CmcIdToTagNames
    all_tag_names: set[str]
