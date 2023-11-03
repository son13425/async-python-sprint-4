from models.links_model import LinksModel
from schemas.links import LinksCreate

from datetime import datetime
from models import User
from sqlalchemy.ext.asyncio import AsyncSession
from services.creators import get_unique_short_id


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
        new_link_data['short'] = get_unique_short_id()
    if new_link_data['password'] in [None, ""]:
        new_link_data['password'] = None
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
