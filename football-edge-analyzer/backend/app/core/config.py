from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Football Edge Analyzer"
    environment: str = "local"
    database_url: str = "sqlite:///./football_edge.db"

    flashscore_base_url: str | None = None
    flashscore_api_key: str | None = None
    flashscore_client_id: str | None = None
    flashscore_client_secret: str | None = None
    flashscore_rate_limit_per_minute: int = 60
    flashscore_timeout_seconds: int = 15
    flashscore_provider_enabled: bool = False

    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    openrouter_api_key: str | None = None
    openrouter_model: str = "poolside/laguna-m.1:free"
    openrouter_enabled: bool = False
    openrouter_timeout_seconds: int = 30
    openrouter_site_url: str | None = None
    openrouter_app_title: str = "Football Edge Analyzer"

    min_ev: float = 0.10
    strong_ev: float = 0.15
    min_confidence_score: int = 60
    min_odd: float = 1.50
    max_odd: float = 4.00

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
