from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from application.api.admin import router as admin_router
from application.api.auth import router as auth_router
from application.api.category import router as category_router
from application.api.comment import router as comment_router
from application.api.location import router as location_router
from application.api.post import router as post_router
from application.api.user import router as user_router
from application.core.config import settings


def create_app() -> FastAPI:
    app = FastAPI(root_path=settings.ROOT_PATH)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            host.strip() for host in settings.ORIGINS.split(',') if host.strip()
        ],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    app.include_router(auth_router, prefix='/auth', tags=['Auth'])
    app.include_router(admin_router, prefix='/admin')
    app.include_router(user_router, prefix='/user', tags=['User'])
    app.include_router(category_router, prefix='/category', tags=['Category'])
    app.include_router(location_router, prefix='/location', tags=['Location'])
    app.include_router(post_router, prefix='/post', tags=['Post'])
    app.include_router(comment_router, prefix='/comment', tags=['Comment'])

    return app
