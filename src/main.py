import logging

import uvicorn

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from core.config import settings
from core.logger import LOGGING


app = FastAPI(
    # Конфигурируем название проекта. Оно будет отображаться в документации
    title=settings.name,
    # Адрес документации в красивом интерфейсе
    docs_url='/api/openapi',
    # Адрес документации в формате OpenAPI
    openapi_url='/api/openapi.json',
    # замена стандартного JSON-сериализатора на более шуструю версию, написанную на Rust
    default_response_class=ORJSONResponse,
)

# # Подключаем роутер к серверу, указав префикс /v1
# app.include_router(base.router, prefix='/api/v1')


if __name__ == '__main__':
    # чтобы иметь возможность использовать дебагер,
    # запустим uvicorn сервер через python
    uvicorn.run(
        'main:app',
        host=settings.host,
        port=settings.port,
        reload=True
    )
