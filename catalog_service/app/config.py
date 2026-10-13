from pydantic_settings import BaseSettings, SettingsConfigDict

class Config(BaseSettings):
    DATABASE_CATALOG_URL: str
    AUTH_SERVICE_URL: str

    # Указываем в model config путь к env файлу
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

config = Config()

