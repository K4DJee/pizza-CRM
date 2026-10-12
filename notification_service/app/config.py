from pydantic_settings import BaseSettings, SettingsConfigDict

class Config(BaseSettings):
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_SERVER: str

    # Указываем в model config путь к env файлу
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

config = Config()

