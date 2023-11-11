from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from core.user import auth_backend, fastapi_users
from schemas.user import UserCreate, UserRead, UserUpdate

router = APIRouter()


# вход/выход
router.include_router(
    # В роутер аутентификации
    # передается объект бэкенда аутентификации.
    fastapi_users.get_auth_router(auth_backend),
    prefix='/auth/jwt',
    tags=['auth'],
)
# регистрация
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix='/auth',
    tags=['auth'],
)
# управление пользователем
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix='/users',
    tags=['users'],
)


@router.delete(
    # Путь и тег полностью копируют параметры эндпоинта по умолчанию.
    '/users/{id}',
    tags=['users'],
    # Параметр, который показывает, что метод устарел.
    deprecated=True
)
def delete_user(id: str):
    """Не используйте удаление, деактивируйте пользователей."""
    raise HTTPException(
        # 405 ошибка - метод не разрешен.
        status_code=HTTPStatus.METHOD_NOT_ALLOWED,
        detail="Удаление пользователей запрещено!"
    )
