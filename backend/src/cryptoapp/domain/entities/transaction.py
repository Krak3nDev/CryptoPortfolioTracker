import datetime
from dataclasses import dataclass
from typing import NewType

from cryptoapp.domain.entities.asset import AssetId

TransactionId = NewType("TransactionId", int)


@dataclass
class Transaction:
    id: TransactionId
    asset_id: AssetId
    amount: float
    price: float
    date: datetime.datetime
