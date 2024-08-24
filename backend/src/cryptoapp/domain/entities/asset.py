from dataclasses import dataclass
from decimal import Decimal
from typing import NewType

AssetId = NewType("AssetId", int)


@dataclass
class Asset:
    id: AssetId
    name: str
    symbol: str
    slug: str
    price: Decimal
    percent_change_1h: float
    percent_change_24h: float
    percent_change_7d: float
