from models.query_data import QueryDataModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


async def add_query_data(
    query_data: dict,
    session: AsyncSession,
) -> None:
    """
    Добавляет информацию о запросе оригинальной
    ссылки в базу данных
    """
    db_query_data = QueryDataModel(**query_data)
    session.add(db_query_data)
    await session.commit()


async def read_all_querys_link_from_db(
    short_link_id: int,
    session: AsyncSession
) -> list[QueryDataModel]:
    """Возвращает список всех запросов короткой ссылки"""
    db_querys_link = await session.execute(
        select(QueryDataModel).where(
            QueryDataModel.short_link_id == short_link_id
        )
    )
    return db_querys_link.scalars().all()