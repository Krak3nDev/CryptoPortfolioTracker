from typing import TypedDict


class CryptoCurrencyQuoteUSD(TypedDict):
    price: float
    volume_24h: float
    volume_change_24h: float
    percent_change_1h: float
    percent_change_24h: float
    percent_change_7d: float
    percent_change_30d: float
    percent_change_60d: float
    percent_change_90d: float
    market_cap: float
    market_cap_dominance: float
    fully_diluted_market_cap: float
    tvl: float | None
    last_updated: str  # ISO format datetime string


class CryptoCurrencyQuote(TypedDict):
    USD: CryptoCurrencyQuoteUSD


class CryptoCurrencyPlatform(TypedDict):
    id: int
    name: str
    symbol: str
    slug: str
    token_address: str


class CryptoCurrency(TypedDict):
    id: int
    name: str
    symbol: str
    slug: str
    num_market_pairs: int
    date_added: str  # ISO format datetime string
    tags: list[str]
    max_supply: float | None
    circulating_supply: float
    total_supply: float
    infinite_supply: bool
    platform: CryptoCurrencyPlatform | None
    cmc_rank: int
    self_reported_circulating_supply: float | None
    self_reported_market_cap: float | None
    tvl_ratio: float | None
    last_updated: str  # ISO format datetime string
    quote: CryptoCurrencyQuote


class CryptoCurrencyListingStatus(TypedDict):
    timestamp: str  # ISO format datetime string
    error_code: int
    error_message: str | None
    elapsed: int
    credit_count: int
    notice: str | None
    total_count: int


class CryptoCurrencyListingResponse(TypedDict):
    status: CryptoCurrencyListingStatus
    data: list[CryptoCurrency]
