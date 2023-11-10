import os
from logging import config as logging_config
from typing import Optional

from pydantic import BaseSettings, EmailStr, PostgresDsn

from core.logger import LOGGING

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)

# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Settings(BaseSettings):
    name: str = 'Укорачиватель ссылок'
    host: str = '0'
    port: int = 8000
    database_dsn: PostgresDsn = (
        'postgresql+asyncpg://postgres:postgres@localhost:6000/postgres'
    )
    secret: str = 'SECRET'
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None

    class Config:
        env_file = '.env'


settings = Settings()

# Допустимый размер ссылок
ORIGINAL_LEN = 2048
SHORT_LEN = 16
URL_SHORT_LEN = 36
CUSTOM_ID_LEN = 6
