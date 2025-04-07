import datetime

from pydantic import BaseModel
from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from src.infrastructure.database.metadata import Base


class TimestampMixin(Base):
    __abstract__ = True

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        server_default=func.now()
    )


class TimestampDTOMixin(BaseModel):
    created_at: datetime.datetime
