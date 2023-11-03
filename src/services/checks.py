from sqlalchemy.ext.asyncio import AsyncSession
from models.links_model import LinksModel
from sqlalchemy import select


async def check_uniq_short(
    short: str,
    session: AsyncSession
) -> bool:
    """Проверка уникальности короткой ссылки"""
    short_links = await session.execute(
        select(LinksModel.id).where(
            LinksModel.short == short
        )
    )
    short_link_id = short_links.scalars().first()
    return short_link_id
