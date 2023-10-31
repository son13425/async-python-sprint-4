from datetime import datetime
from sqlalchemy import Column, DateTime, String

from db.db import Base
from core.config import ORIGINAL_LEN, SHORT_LEN


class LinksModel(Base):
    """Модель таблицы ссылок"""
    original = Column(String(ORIGINAL_LEN), nullable=False)
    short = Column(String(SHORT_LEN), unique=True, nullable=False)
    timestamp = Column(DateTime, index=True, default=datetime.utcnow)
    password = Column(String(SHORT_LEN), unique=True, nullable=True)
    status = Column(String(6), nullable=False)
