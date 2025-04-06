import datetime

from pydantic import BaseModel
from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from src.infrastructure.database.metadata import Base


class TimestampMixin(Base):
    __abstract__ = True

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        default=datetime.datetime.now(datetime.UTC).replace(tzinfo=None)
    )
    updated_at: Mapped[datetime.datetime | None] = mapped_column(
        DateTime,
        default=datetime.datetime.now(datetime.UTC).replace(tzinfo=None),
        onupdate=datetime.datetime.now(datetime.UTC).replace(tzinfo=None),
    )


class TimestampDTOMixin(BaseModel):
    created_at: datetime.datetime
    updated_at: datetime.datetime | None
