from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable

from db.db import Base

class User(SQLAlchemyBaseUserTable[int], Base):
    """Модель User"""
    pass
