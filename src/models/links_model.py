from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String

from core.config import ORIGINAL_LEN, SHORT_LEN, URL_SHORT_LEN
from db.db import Base


class LinksModel(Base):
    """Модель таблицы ссылок"""
    original = Column(String(ORIGINAL_LEN), nullable=False)
    short = Column(String(SHORT_LEN), unique=True, nullable=False)
    url_short = Column(String(URL_SHORT_LEN), nullable=False)
    timestamp = Column(DateTime, index=True, default=datetime.utcnow)
    password = Column(String(SHORT_LEN), default=None)
    is_active = Column(Boolean, default=True)
    user_id = Column(Integer, ForeignKey('user.id'))
