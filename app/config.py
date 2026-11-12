from functools import lru_cache

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Барлық құпия мәндер тек .env файлынан оқылады."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    bot_token: SecretStr
    database_url: SecretStr
    gemini_api_key: SecretStr = SecretStr("")
    admin_ids: str = ""  # "12345,67890"
    default_subject: str = "world_history"
    log_level: str = "INFO"

    @property
    def admin_id_set(self) -> set[int]:
        return {int(x) for x in self.admin_ids.replace(" ", "").split(",") if x.isdigit()}


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]
