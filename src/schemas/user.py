from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    """Вернуть объект User"""
    pass


class UserCreate(schemas.BaseUserCreate):
    """Создать объект User"""
    pass


class UserUpdate(schemas.BaseUserUpdate):
    """Обновить объект User"""
    pass
