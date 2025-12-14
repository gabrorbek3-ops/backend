from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    API_ID: int
    API_HASH: str
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int
    DB_URL: str
    DEBUG: bool

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings() # type: ignore