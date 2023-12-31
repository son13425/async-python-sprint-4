from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class QueryDataBase(BaseModel):
    """Базовая схема для записи информации о запросе"""
    short_link_id: Optional[str]
    ip_client: Optional[str]
    timestamp: Optional[datetime]

    class Config:
        orm_mode = True


class QueryData(BaseModel):
    """Схема ответа на запрос информации о запросе ссылки"""
    ip_client: str
    timestamp: datetime


class AllQueryLinkDB(BaseModel):
    """Cхема ответа на запрос активности использования ссылки"""
    short_link_id: str
    count_querys: int
    querys: list[QueryData]

    class Config:
        orm_mode = True
