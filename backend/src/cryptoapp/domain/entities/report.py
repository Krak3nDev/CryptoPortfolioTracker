import datetime
from dataclasses import dataclass
from typing import NewType

from .user_id import UserId

ReportId = NewType("ReportId", int)


@dataclass
class Report:
    id: ReportId
    user_id: UserId
    # report_data: ...
    date: datetime.datetime
