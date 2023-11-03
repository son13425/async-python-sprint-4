from typing import Optional
...
from models import User

...

async def create(
        self,
        obj_in,
        session: AsyncSession,
        # Добавьте опциональный параметр user.
        user: Optional[User] = None
):
    obj_in_data = obj_in.dict()
    # Если пользователь был передан...
    if user is not None:
        # ...то дополнить словарь для создания модели.
        obj_in_data['user_id'] = user.id
    db_obj = self.model(**obj_in_data)
    session.add(db_obj)
    await session.commit()
    await session.refresh(db_obj)
    return db_obj
