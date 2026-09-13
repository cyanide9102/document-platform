from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[4]


class PostgresSettings(BaseModel):
    host: str
    port: int = 5432
    user: str
    password: str
    database: str


class TemporalSettings(BaseModel):
    host: str
    task_queue: str
    namespace: str = "default"


class Settings(BaseSettings):
    postgres: PostgresSettings
    temporal: TemporalSettings

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://"
            f"{self.postgres.user}:{self.postgres.password}@"
            f"{self.postgres.host}:{self.postgres.port}/"
            f"{self.postgres.database}"
        )

    @property
    def storage_path(self) -> Path:
        return PROJECT_ROOT / "storage"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="ignore",
    )


settings = Settings()
