import logging

import uvicorn

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.routers import main_router
from core.config import settings
from core.logger import LOGGING


app = FastAPI(
    # Конфигурируем название проекта. Оно будет отображаться в документации
    title=settings.name,
    default_response_class=ORJSONResponse,
)

# # Подключаем роутер к серверу
app.include_router(main_router)


if __name__ == '__main__':
    # чтобы иметь возможность использовать дебагер,
    # запустим uvicorn сервер через python
    uvicorn.run(
        'main:app',
        host=settings.host,
        port=settings.port,
        reload=True
    )
