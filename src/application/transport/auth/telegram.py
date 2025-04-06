from pydantic import BaseModel


class TelegramUserDTO(BaseModel):
    id: int
    first_name: str
    last_name: str | None = None
    username: str | None = None
    language_code: str | None = None
    is_premium: bool = False
    photo_url: str | None = None
    allows_write_to_pm: bool = False


class TelegramInitDataDTO(BaseModel):
    user: TelegramUserDTO
    chat_instance: str | None = None
    chat_type: str | None = None
    start_param: str | None = None
    auth_date: int
    signature: str
    hash: str
