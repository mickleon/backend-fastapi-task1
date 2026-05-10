from fastapi import APIRouter

from application.api.admin_api.category import router as category_router
from application.api.admin_api.comment import router as comment_router
from application.api.admin_api.location import router as location_router
from application.api.admin_api.post import router as post_router
from application.api.admin_api.user import router as user_router

router = APIRouter()

router.include_router(user_router, prefix='/user', tags=['User admin'])
router.include_router(
    category_router, prefix='/category', tags=['Category admin']
)
router.include_router(
    location_router, prefix='/location', tags=['Location admin']
)
router.include_router(post_router, prefix='/post', tags=['Post admin'])
router.include_router(comment_router, prefix='/comment', tags=['Comment admin'])
