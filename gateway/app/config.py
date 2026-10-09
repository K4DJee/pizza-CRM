from pydantic_settings import SettingsConfigDict, BaseSettings

class Config(BaseSettings):
    AUTH_SERVICE_URL: str
    ORDER_SERVICE_URL: str

    JWT_ACCESS_SECRET_KEY: str
    JWT_REFRESH_SECRET_KEY: str
    ALGORITHM: str = "HS256" # Можно задать значение по умолчанию
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int


    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

config = Config()