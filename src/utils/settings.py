from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    CONNECTION: str
    Algorithm: str = "HS256"
    Secret_key: str
    EXP_TIME: int = 60  # minutes


settings = Settings()
