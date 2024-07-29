from dataclasses import dataclass
from typing import NewType

AssetId = NewType("AssetId", int)


@dataclass
class Asset:
    id: AssetId
    name: str
    symbol: str
    usdt_price: float
    slug: str
