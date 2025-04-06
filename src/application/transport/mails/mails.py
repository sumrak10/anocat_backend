from pydantic import BaseModel, model_validator

from src.application.transport.users.users_info import UserInfoDTO
from src.utils.models.mixins import TimestampDTOMixin


class MailDTO(TimestampDTOMixin, BaseModel):
    id: int
    text: str
    is_read: bool


class InboxMailDTO(MailDTO):
    sender_id: int | None
    sender: UserInfoDTO | None
    is_anonymous: bool

    is_blocked_by_stop_words: bool = False

    def anonymize_sender(self):
        self.sender_id = None
        self.sender = None


class SentMailDTO(MailDTO):
    receiver_id: int
    receiver: UserInfoDTO | None


class MailCreateDTO(BaseModel):
    receiver_id: int
    text: str
    is_anonymous: bool
