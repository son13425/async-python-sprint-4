from core.user import current_user
from models import User
from fastapi import APIRouter, Depends,  HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from db.db import get_session

from crud.links import create_new_short_link
from schemas.links import LinksCreate, LinksDB
from services.checks import check_uniq_short

router = APIRouter()


@router.post(
    '/link/',
    response_model=LinksDB,
    response_model_exclude_none=True
)
async def create_new_link(
        link: LinksCreate,
        session: AsyncSession = Depends(get_session),
        user: User = Depends(current_user)
):
    """Создает новую короткую ссылку"""
    short_link_id = await check_uniq_short(link.short, session)
    if short_link_id is not None:
        raise HTTPException(
            status_code=422,
            detail='Такая короткая ссылка уже существует!',
        )
    new_link = await create_new_short_link(link, session, user)
    return new_link
