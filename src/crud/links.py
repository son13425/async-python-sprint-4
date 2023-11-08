from datetime import datetime
from typing import Optional, Any

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from models import User
from models.links_model import LinksModel
from schemas.links import LinksCreate, LinksUserDB
from services.creators import create_unique_short_link


async def create_new_short_link(
    new_link: LinksCreate,
    session: AsyncSession,
    user: User
) -> LinksModel:
    """Добавляет новую ссылку в базу данных"""
    new_link_data = new_link.dict()
    timestamp = datetime.now()
    new_link_data['timestamp'] = timestamp
    new_link_data['user_id'] = user.id
    if new_link_data['short'] in [None, ""]:
        new_link_data['short'] = create_unique_short_link()
    if new_link_data['password'] in [None, ""]:
        new_link_data['password'] = None
    short_link = new_link_data['short']
    url_link = f'http://{settings.host}:{settings.port}/{short_link}'
    new_link_data['url_short'] = url_link
    db_link = LinksModel(**new_link_data)
    session.add(db_link)
    await session.commit()
    await session.refresh(db_link)
    return db_link


async def read_all_links_from_db(
    session: AsyncSession,
) -> list[LinksModel]:
    """Возвращает список всех ссылок в базе"""
    db_links = await session.execute(select(LinksModel))
    return db_links.scalars().all()


async def update_link_db(
    link_obj: LinksModel,
    dict_data: dict,
    session: AsyncSession
) -> LinksModel:
    """Обновляет ссылку"""
    obj_data = jsonable_encoder(link_obj)
    update_data = dict_data
    for field in obj_data:
        if field in update_data:
            setattr(link_obj, field, update_data[field])
    session.add(link_obj)
    await session.commit()
    await session.refresh(link_obj)
    return link_obj


async def get_link_id(
    short_link: str,
    session: AsyncSession
) -> Optional[int]:
    """Возвращает id ссылки"""
    links_id = await session.execute(
        select(LinksModel.id).where(
            LinksModel.short == short_link
        )
    )
    link_id = links_id.scalars().first()
    return link_id


async def get_link_obj(
    short_link: str,
    session: AsyncSession
) -> LinksModel:
    """Возвращает объект БД для ссылки"""
    links_obj = await session.execute(
        select(LinksModel).where(
            LinksModel.short == short_link
        )
    )
    link_obj = links_obj.scalars().first()
    return link_obj


async def read_all_links_user_from_db(
    user_id: int,
    session: AsyncSession
) -> list[dict[str, Any]]:
    """Возвращает все ссылки текущего юзера"""
    db_objs = await session.execute(
        select(LinksModel).where(
            LinksModel.user_id == user_id
        )
    )
    list_objs = db_objs.scalars().all()
    list_links = []
    for obj in list_objs:
        if obj.password is None:
            type_link = 'public'
        else:
            type_link = 'private'
        if obj.is_active:
            status_link = 'active'
        else:
            status_link = 'delete'
        list_links.append({
            'short-id': obj.short,
            'short-url': obj.url_short,
            'original-url': obj.original,
            'type': type_link,
            'status': status_link
        })
    return list_links
