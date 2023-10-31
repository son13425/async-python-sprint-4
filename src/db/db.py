from core.config import settings
from sqlalchemy import Column, Integer
from sqlalchemy.orm import declarative_base, declared_attr, sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession


class PreBase:
    """Базовый класс для моделей таблиц базы данных"""
    @declared_attr
    def __tablename__(cls):
        # Именем таблицы будет название модели в нижнем регистре.
        return cls.__name__.lower()

    # Во все таблицы будет добавлено поле ID.
    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=PreBase)

# Создаём движок
# Настройки подключения к БД передаём из переменных окружения,
# которые заранее загружены в файл настроек
engine = create_async_engine(
    settings.database_dsn,
    echo=True,
    future=True
)
async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Функция понадобится при внедрении зависимостей
# Dependency
async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
