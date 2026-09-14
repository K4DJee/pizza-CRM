from pydantic_settings import BaseSettings, SettingsConfigDict

class Config(BaseSettings):
    JWT_ACCESS_SECRET_KEY: str
    JWT_REFRESH_SECRET_KEY: str
    ALGORITHM: str = "HS256" # Можно задать значение по умолчанию
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_SERVER: str

    # Указываем в model config путь к env файлу
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

config = Config()

