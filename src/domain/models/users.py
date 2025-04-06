from sqlalchemy import BigInteger, Index
from sqlalchemy.orm import Mapped, mapped_column

from src.application.transport.users.users import UserDTO
from src.infrastructure.database.metadata import Base
from src.utils.models.mixins import TimestampMixin


class UserModel(TimestampMixin, Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger(), primary_key=True, autoincrement=False)
    first_name: Mapped[str]
    last_name: Mapped[str | None]
    username: Mapped[str | None]
    language_code: Mapped[str | None]
    is_premium: Mapped[bool | None]
    allows_write_to_pm: Mapped[bool | None]
    photo_url: Mapped[str | None]

    is_active: Mapped[bool] = mapped_column(default=True)

    def to_dto(self) -> UserDTO:
        return UserDTO.model_validate(self, from_attributes=True)
