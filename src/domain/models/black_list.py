from sqlalchemy.orm import Mapped, mapped_column
from src.infrastructure.database.metadata import Base
from src.utils.models.mixins import TimestampMixin
from src.utils.models.sqla_types import TelegramFK


class BlackListItemModel(TimestampMixin, Base):
    __tablename__ = "users__black_list"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[TelegramFK]
    blocked_id: Mapped[TelegramFK]
