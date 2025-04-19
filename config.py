from aiogram.types import Message
from pydantic_settings import BaseSettings, SettingsConfigDict
import os

root_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(root_dir, '.env')


class CoreSettings(BaseSettings):
    model_config = SettingsConfigDict(  # configuring .env file
        env_file=env_path,
        env_file_encoding='utf-8',
        extra="ignore")  # ignoring other secret keys


class AppSettings(CoreSettings):
    BOT_TOKEN: str


class DBSettings(CoreSettings):
    DB_URL: str



db_settings = DBSettings()
app_settings = AppSettings()

