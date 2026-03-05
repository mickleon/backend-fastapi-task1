from fastapi import APIRouter

from src.api.base.user import user_router
from src.api.base.category import category_router

base_router = APIRouter()
base_router.include_router(user_router, prefix='/user')
base_router.include_router(category_router, prefix='/category')
