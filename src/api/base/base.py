from fastapi import APIRouter

from src.api.base.user import user_router
from src.api.base.category import category_router
from src.api.base.location import location_router
from src.api.base.post import post_router

base_router = APIRouter()

base_router.include_router(user_router, prefix='/user')
base_router.include_router(category_router, prefix='/category')
base_router.include_router(location_router, prefix='/location')
base_router.include_router(post_router, prefix='/post')

