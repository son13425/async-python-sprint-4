from sqlalchemy.ext.asyncio import AsyncSession

from crud.links import get_link_id


async def check_uniq_short(
    short: str,
    session: AsyncSession
) -> bool:
    """Проверка уникальности короткой ссылки"""
    short_link_id = await get_link_id(short, session)
    if not short_link_id:
        return True
    return False


async def chek_user_is_author(
    link_obj_user_id: int,
    current_user_id: int
) -> bool:
    """Проверяет, является ли текущий юзер автором ссылки"""
    if current_user_id == link_obj_user_id:
        return True
    return False
