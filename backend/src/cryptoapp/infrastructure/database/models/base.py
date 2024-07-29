import datetime

from sqlalchemy.orm import Mapped, declared_attr, mapped_column
from sqlalchemy.orm.decl_api import DeclarativeBase
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import TIMESTAMP, Integer
from typing_extensions import Annotated


class Base(DeclarativeBase):
    pass


# Mixins
class TimestampMixin:
    created_at: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )


class TableNameMixin:
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + "s"  # type: ignore


# Common column types
int_pk = Annotated[int, mapped_column(Integer, primary_key=True, index=True)]
