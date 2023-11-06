from typing import Optional
from pydantic import BaseModel, Field
from core.config import ORIGINAL_LEN, SHORT_LEN
from datetime import datetime


class LinksBase(BaseModel):
    """Базовая схема для операции создания ссылки"""
    original: Optional[str] = Field(None, max_length=ORIGINAL_LEN)
    short: Optional[str] = Field(None, max_length=SHORT_LEN)
    password: Optional[str] = Field(None, max_length=SHORT_LEN)
    is_active: Optional[bool] = Field(None, alias='is-active')

    class Config:
        orm_mode = True


class LinksCreate(LinksBase):
    """Схема для создания ссылки"""
    original: str = Field(..., max_length=ORIGINAL_LEN)
    is_active: bool = Field(True, alias='is-active')


class LinksDB(LinksBase):
    """Схема для ответа на создание ссылки"""
    id: int
    user_id: int
    timestamp: datetime
    is_active: bool


class LinkOriginalDB(LinksBase):
    """Схема для ответа на запрос оригинальной ссылки"""
    original: str = Field(..., max_length=ORIGINAL_LEN)


class LinksAllDB(BaseModel):
    """Схема для ответа на запрос всех ссылок"""
    count_links: int
    links: list[LinksDB]

    class Config:
        orm_mode = True