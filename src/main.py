import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.routers import main_router
from core.config import settings
from core.init_db import create_first_superuser

app = FastAPI(
    title=settings.name,
    default_response_class=ORJSONResponse,
)

app.include_router(main_router)


@app.on_event('startup')
async def startup():
    await create_first_superuser()


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=settings.host,
        port=settings.port,
        reload=True
    )
