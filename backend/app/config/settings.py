from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    db_driver: str
    db_host: str
    db_port: int
    db_name: str
    db_user: str = Field(alias='pg_user')
    db_password: str = Field(alias='pg_pw')
    debug_mode: bool = True
    model_config = SettingsConfigDict(secrets_dir='/run/secrets',env_file=f"{os.getcwd()}/app/.env", env_file_encoding="utf-8", extra="ignore")

# Load config for app
settings = Settings()