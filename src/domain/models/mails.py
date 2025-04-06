from sqlalchemy import BigInteger, Index
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.database.metadata import Base
from src.utils.models.mixins import TimestampMixin
from src.utils.models.sqla_types import TelegramFK


class MailModel(TimestampMixin, Base):
    __tablename__ = "mails"

    id: Mapped[int] = mapped_column(BigInteger(), primary_key=True, autoincrement=True)
    sender_id: Mapped[TelegramFK]
    receiver_id: Mapped[TelegramFK]
    text: Mapped[str]
    is_anonymous: Mapped[bool]
    is_read: Mapped[bool] = mapped_column(default=False)
    # System filters
    is_deleted_by_receiver: Mapped[bool] = mapped_column(default=False)
    is_deleted_by_sender: Mapped[bool] = mapped_column(default=False)
    is_spam: Mapped[bool] = mapped_column(default=False)

    __table_args__ = (
        Index('ix_mails_sender_id', 'sender_id'),
        Index('ix_mails_receiver_id', 'receiver_id'),
        Index('ix_mails_id_sender_id', 'id', 'sender_id'),
        Index('ix_mails_id_receiver_id', 'id', 'receiver_id'),
    )
