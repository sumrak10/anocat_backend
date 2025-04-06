from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="SENTRY_",
        extra="ignore",
    )

    DSN: str
    TRACES_SAMPLE_RATE: float = 1.0


sentry_settings = Settings()
