import os
from logging import config as logging_config
from pydantic import BaseSettings,  PostgresDsn

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

    class Config:
        env_file = '.env'


settings = Settings()

# Допустимый размер ссылок
ORIGINAL_LEN = 2048
SHORT_LEN = 16
CUSTOM_ID_LEN = 6
