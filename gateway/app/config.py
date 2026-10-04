from pydantic_settings import SettingsConfigDict, BaseSettings

class Config(BaseSettings):
    AUTH_SERVICE_URL: str
    ORDER_SERVICE_URL: str


    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

config = Config()