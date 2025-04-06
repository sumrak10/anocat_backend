import hashlib

from pydantic_settings import BaseSettings, SettingsConfigDict

from src.config.app import app_settings


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix='TELEGRAM_API_',
        extra="ignore",
    )

    TOKEN: str
    BOT_USERNAME: str
    WEBHOOK_PATH: str
    WEBHOOK_SECRET: str

    ADMIN_IDS: list[int]

    WEB_APP_PATH: str | None = None

    def get_web_app_url(self) -> str:
        if self.WEB_APP_PATH is not None:
            return app_settings.URL + self.WEB_APP_PATH
        return app_settings.URL

    def get_secret_key(self) -> bytes:
        return hashlib.sha256(self.TOKEN.encode()).digest()


telegram_settings = Settings()
