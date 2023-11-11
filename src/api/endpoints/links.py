from datetime import datetime
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from core.user import current_user
from crud.links import (create_new_short_link, get_link_id, get_link_obj,
                        read_all_links_from_db, read_all_links_user_from_db,
                        update_link_db)
from crud.query_data import add_query_data, read_all_querys_link_from_db
from db.db import get_session
from models import User
from schemas.links import (AllLinksUserDB, AnswerLinkOriginal, LinkOriginalDB,
                           LinkPassword, LinksAllDB, LinksCreate, LinksDB,
                           LinksUpdate, LinkUpdateDB, RequestLinkOriginal)
from schemas.query_data import AllQueryLinkDB
from services.checks import check_uniq_short, chek_user_is_author

router = APIRouter()


@router.post(
    '/link',
    response_model=LinksDB,
    response_model_exclude_none=True
)
async def create_new_link(
        link: LinksCreate,
        session: AsyncSession = Depends(get_session),
        user: User = Depends(current_user)
):
    """Создает новую короткую ссылку"""
    short_link_uniq = await check_uniq_short(link.short, session)
    if not short_link_uniq:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Такая короткая ссылка уже существует!',
        )
    new_link = await create_new_short_link(link, session, user)
    return new_link


@router.post(
    '/links',
    response_model=list[AnswerLinkOriginal],
    response_model_exclude_none=True
)
async def create_new_links(
        links: list[RequestLinkOriginal],
        session: AsyncSession = Depends(get_session),
        user: User = Depends(current_user)
):
    """Создает новые короткие ссылки по списку (batch upload)"""
    list_short_links = []
    for link in links:
        link_original = {'original': link.dict()['original_url']}
        link_query = LinksCreate(**link_original)
        new_link = await create_new_short_link(link_query, session, user)
        list_short_links.append({
            'short-id': new_link.short,
            'short-url': new_link.url_short
        })
    return list_short_links


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
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Доступно только суперюзеру',
        )
    all_links = await read_all_links_from_db(session)
    if all_links is None:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='В базе данных нет записей',
        )
    count_links = len(all_links)
    return {'count_links': count_links, 'links': all_links}


@router.post(
    '/{short_link}',
    response_model=LinkOriginalDB,
    response_model_exclude_none=True,
)
async def get_original_link(
    short_link: str,
    password: LinkPassword,
    request: Request,
    session: AsyncSession = Depends(get_session)
):
    """Возвращает оригинальную ссылку по короткой"""
    link_obj = await get_link_obj(short_link, session)
    if link_obj is None:
        raise HTTPException(
            status_code=HTTPStatus.GONE,
            detail='Такая короткая ссылка не существует!',
        )
    if link_obj.is_active is False:
        raise HTTPException(
            status_code=HTTPStatus.GONE,
            detail='Cсылка не существует!',
        )
    dict_short_request = {
        'short_link_id': link_obj.id,
        'ip_client': request.client.host,
        'timestamp': datetime.now()
    }
    await add_query_data(dict_short_request, session)
    if link_obj.password is None:
        original_link = link_obj.original
        return {'original': original_link}
    password_link = password.dict()['password']
    if not password_link:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Введите пароль!',
        )
    elif password_link != link_obj.password:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Неверный пароль!',
        )
    original_link = link_obj.original
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
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Доступно только суперюзеру',
        )
    short_link_id = await get_link_id(short_link, session)
    if short_link_id is None:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Такая короткая ссылка не существует!',
        )
    all_querys_link = await read_all_querys_link_from_db(
        short_link_id,
        session
    )
    count_querys_link = len(all_querys_link)
    if count_querys_link == 0:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Ссылку не запрашивали',
        )
    return {
        'short_link_id': short_link_id,
        'count_querys': count_querys_link,
        'querys': all_querys_link
    }


@router.delete(
    '/{short_link}',
    response_model=LinkUpdateDB,
    response_model_exclude_none=True,
)
async def delete_link(
    short_link: str,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(current_user)
):
    """Удаляет ссылку(делает ее неактивной)"""
    link_obj = await get_link_obj(short_link, session)
    if link_obj is None:
        raise HTTPException(
            status_code=HTTPStatus.GONE,
            detail='Такая короткая ссылка не существует!',
        )
    if link_obj.is_active is False:
        raise HTTPException(
            status_code=HTTPStatus.GONE,
            detail='Cсылка не существует!',
        )
    user_is_author = await chek_user_is_author(link_obj.user_id, user.id)
    if (user.is_superuser or user_is_author) is True:
        dict_data = {'is_active': False}
        await update_link_db(link_obj, dict_data, session)
    else:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Доступно только суперюзеру и автору',
        )
    return {'message': 'Ссылка успешно удалена'}


@router.patch(
    '/{short_link}',
    response_model=LinkUpdateDB,
    response_model_exclude_none=True
)
async def partially_update_link(
    short_link: str,
    link_obj_in: LinksUpdate,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(current_user)
):
    """Обновляет объект ссылки в БД"""
    link_obj = await get_link_obj(short_link, session)
    if link_obj is None:
        raise HTTPException(
            status_code=HTTPStatus.GONE,
            detail='Такая короткая ссылка не существует!',
        )
    user_is_author = await chek_user_is_author(link_obj.user_id, user.id)
    if (user.is_superuser or user_is_author) is True:
        dict_data = link_obj_in.dict(exclude_unset=True)
        await update_link_db(link_obj, dict_data, session)
        return {'message': 'Ссылка успешно отредактирована'}
    raise HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Доступно только суперюзеру и автору',
    )


@router.get(
    '/user/status',
    response_model=AllLinksUserDB,
    response_model_exclude_none=True,
)
async def get_all_links_user(
    session: AsyncSession = Depends(get_session),
    user: User = Depends(current_user)
):
    """Возвращает информацию обо всех ссылках, созданных юзером"""
    all_links_user = await read_all_links_user_from_db(user.id, session)
    count_links = len(all_links_user)
    if count_links == 0:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Пользователь не создавал ссылок',
        )
    return {
        'count_links': count_links,
        'links': all_links_user
    }
