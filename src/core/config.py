import os
from logging import config as logging_config
from pydantic import BaseSettings,  PostgresDsn, EmailStr
from typing import Optional

from core.logger import LOGGING

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)

# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Settings(BaseSettings):
    name: str
    host: str
    port: int
    database_dsn: PostgresDsn
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
