from pydantic import BaseModel

from src.application.transport.auth.telegram import TelegramUserDTO
from src.utils.models.mixins import TimestampDTOMixin


class UserInDBPartDTO(BaseModel):
    is_active: bool


class UserDTO(TimestampDTOMixin, TelegramUserDTO, UserInDBPartDTO):
    pass

    def get_full_name(self):
        if self.last_name is not None:
            return f"{self.first_name} {self.last_name}"
        return self.first_name
