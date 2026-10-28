from pydantic_settings import SettingsConfigDict, BaseSettings

class Config(BaseSettings):
    AUTH_SERVICE_URL: str
    KITCHEN_SERVICE_URL: str
    CATALOG_SERVICE_URL: str
    DATABASE_ORDER_URL: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

config = Config()