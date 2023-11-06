from core.user import current_user
from models import User
from fastapi import APIRouter, Depends,  HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from db.db import get_session

from crud.links import (create_new_short_link,
                        read_all_links_from_db,
                        get_original_link_by_short)
from crud.query_data import add_query_data, read_all_querys_link_from_db
from schemas.links import LinksCreate, LinksDB, LinkOriginalDB, LinksAllDB
from schemas.query_data import AllQueryLinkDB
from services.checks import check_uniq_short
from datetime import datetime


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


@router.get(
    '/links',
    response_model=LinksAllDB,
    response_model_exclude_none=True,
)
async def get_all_links(
    session: AsyncSession = Depends(get_session),
    user: User = Depends(current_user)
):
    """Возвращает все ссылки из базы"""
    if not user.is_superuser:
        raise HTTPException(
            status_code=401,
            detail='Доступно только суперюзеру',
        )
    all_links = await read_all_links_from_db(session)
    if all_links is None:
        raise HTTPException(
            status_code=422,
            detail='В базе данных нет записей',
        )
    count_links = len(all_links)
    return {'count_links': count_links, 'links': all_links}


@router.get(
    '/{short_link}',
    response_model=LinkOriginalDB,
    response_model_exclude_none=True,
)
async def get_original_link(
    short_link: str,
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    """Возвращает оригинальную ссылку по короткой"""
    short_link_id = await check_uniq_short(short_link, session)
    if short_link_id is None:
        raise HTTPException(
            status_code=422,
            detail='Такая короткая ссылка не существует!',
        )
    dict_short_request = {
        'short_link_id': short_link_id,
        'ip_client': request.client.host,
        'timestamp': datetime.now()
    }
    await add_query_data(dict_short_request, session)
    original_link = await get_original_link_by_short(short_link, session)
    return {'original': original_link}


@router.get(
    '/status/{short_link}',
    response_model=AllQueryLinkDB,
    response_model_exclude_none=True,
)
async def get_all_querys_link(
    short_link: str,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(current_user)
):
    """Возвращает информацию обо всех запросах ссылки"""
    if not user.is_superuser:
        raise HTTPException(
            status_code=401,
            detail='Доступно только суперюзеру',
        )
    short_link_id = await check_uniq_short(short_link, session)
    if short_link_id is None:
        raise HTTPException(
            status_code=422,
            detail='Такая короткая ссылка не существует!',
        )
    all_querys_link = await read_all_querys_link_from_db(short_link_id, session)
    count_querys_link = len(all_querys_link)
    if count_querys_link == 0:
        raise HTTPException(
            status_code=422,
            detail='Ссылку не запрашивали',
        )
    return {'count_querys': count_querys_link, 'querys': all_querys_link}