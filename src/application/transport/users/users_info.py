from pydantic import BaseModel


class UserInfoDTO(BaseModel):
    id: int
    first_name: str
    last_name: str | None
    username: str | None = None
    photo_url: str | None

    def get_full_name(self) -> str:
        return f'{self.first_name}{" " if self.last_name else ""}{self.last_name or ""}'
