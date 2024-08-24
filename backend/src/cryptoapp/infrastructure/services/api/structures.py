from datetime import datetime
from typing import Optional, TypedDict, Union


class QuoteCurrency(TypedDict):
    price: float
    volume_24h: float
    volume_change_24h: float
    percent_change_1h: float
    percent_change_24h: float
    percent_change_7d: float
    market_cap: float
    market_cap_dominance: float
    fully_diluted_market_cap: float
    last_updated: str


class Quote(TypedDict):
    USD: QuoteCurrency
    BTC: QuoteCurrency


class CryptoData(TypedDict):
    id: int
    name: str
    symbol: str
    slug: str
    cmc_rank: int
    num_market_pairs: int
    circulating_supply: float
    total_supply: float
    max_supply: Optional[float]
    infinite_supply: bool
    last_updated: str
    date_added: str
    tags: list[str]
    platform: Optional[Union[str, None]]
    self_reported_circulating_supply: Optional[float]
    self_reported_market_cap: Optional[float]
    quote: Quote


class Status(TypedDict):
    timestamp: str
    error_code: int
    error_message: str
    elapsed: int
    credit_count: int


class CryptoResponse(TypedDict):
    data: list[CryptoData]
    status: Status


class DBAssetDict(TypedDict):
    crypto_id: int
    name: str
    symbol: str
    slug: str
    cmc_rank: int
    price: float
    percent_change_1h: float
    percent_change_24h: float
    percent_change_7d: float
    last_updated: datetime
