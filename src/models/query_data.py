from sqlalchemy import Column, DateTime, ForeignKey, Integer, String

from db.db import Base


class QueryDataModel(Base):
    """Модель таблицы информации о запросах"""
    short_link_id = Column(Integer, ForeignKey('linksmodel.id'))
    ip_client = Column(String, nullable=False)
    timestamp = Column(DateTime, index=True, nullable=False)
