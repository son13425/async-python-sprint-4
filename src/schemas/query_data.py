from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class QueryDataBase(BaseModel):
    """Базовая схема для записи информации о запросе"""
    short_link_id: int
    ip_client: str
    timestamp: datetime

    class Config:
        orm_mode = True


class AllQueryLinkDB(BaseModel):
    """Базовая схема ответа о запросе ссылки"""
    count_querys: int
    querys: list[QueryDataBase]

    class Config:
        orm_mode = True
