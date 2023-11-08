from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from core.config import ORIGINAL_LEN, SHORT_LEN, URL_SHORT_LEN


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
    # is_active: bool = Field(True, alias='is-active')


class LinksDB(LinksBase):
    """Схема для ответа на создание ссылки"""
    id: int
    user_id: int
    timestamp: datetime
    is_active: bool
    url_short: str = Field(..., max_length=URL_SHORT_LEN)


class LinkOriginalDB(LinksBase):
    """Схема для ответа на запрос оригинальной ссылки"""
    original: str = Field(..., max_length=ORIGINAL_LEN)


class LinksAllDB(BaseModel):
    """Схема для ответа на запрос всех ссылок"""
    count_links: int
    links: list[LinksDB]

    class Config:
        orm_mode = True


class LinkUpdateDB(BaseModel):
    """Схема для ответа на удаление ссылки"""
    message: str


class LinksUpdate(LinksBase):
    """Схема для обновления ссылки"""
    pass


class LinkPassword(BaseModel):
    """Схема для запроса пароля"""
    password: Optional[str] = Field(None, max_length=SHORT_LEN)


class LinksUserDB(BaseModel):
    """Схема ссылки, созданной текущим юзером"""
    short_id: str = Field(..., alias='short-id')
    short_url: str = Field(..., alias='short-url')
    original_url: str = Field(..., alias='original-url')
    type: str
    status: str


class AllLinksUserDB(BaseModel):
    """Схема для ответа на запрос всех ссылок текущего юзера"""
    count_links: int
    links: list[LinksUserDB]

    class Config:
        orm_mode = True


class RequestLinkOriginal(BaseModel):
    """Схема для запроса списка ссылок для укорачивания (batch upload)"""
    original_url: str = Field(..., alias='original-url')


class AnswerLinkOriginal(BaseModel):
    """Схема для ответа списком ссылок после укорачивания (batch upload)"""
    short_id: str = Field(..., alias='short-id')
    short_url: str = Field(..., alias='short-url')
