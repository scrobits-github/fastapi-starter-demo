"""
App settings from environment variables / .env file.

Copy .env.example → .env and edit if needed.
Never commit real secrets.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Read as DATABASE_URL from the environment.
    # postgresql+psycopg:// works with create_async_engine (psycopg v3 is async-capable).
    database_url: str = (
        "postgresql+psycopg://awesome:awesome@localhost:5433/awesome"
    )


settings = Settings()
