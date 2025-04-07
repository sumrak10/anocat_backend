import hashlib

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix='APP_',
        extra="ignore",
    )

    ENVIRONMENT: str
    LOGGING_LEVEL: int = 10
    URL: str
    VERSION_MAJOR: int
    VERSION_MINOR: int
    VERSION_PATCH: int

    def get_version(self) -> str:
        return f"{self.VERSION_MAJOR}.{self.VERSION_MINOR}.{self.VERSION_PATCH}"

    def get_version_hash(self) -> str:
        return hashlib.sha256(str(self.get_version()).encode()).hexdigest()[:8]


app_settings = Settings()
