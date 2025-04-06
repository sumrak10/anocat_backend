from sqlalchemy import String, Index
from sqlalchemy.orm import Mapped, mapped_column
from src.infrastructure.database.metadata import Base
from src.utils.models.sqla_types import TelegramFK


class StopWordModel(Base):
    __tablename__ = "users__stop_words"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[TelegramFK]
    word: Mapped[str] = mapped_column(String(24), index=True)

    __table_args__ = (
        Index('ix_users__stop_words_user_id', 'user_id'),
    )
