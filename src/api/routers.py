from fastapi import APIRouter

from api.endpoints import (
    user_router,
    link_router
)


main_router = APIRouter()

main_router.include_router(link_router, tags=['links'],)
main_router.include_router(user_router)
