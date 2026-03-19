from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.api.base.user import user_router
from src.api.base.category import category_router
from src.api.base.location import location_router
from src.api.base.post import post_router
from src.api.base.comment import comment_router


def create_app() -> FastAPI:
    app = FastAPI(root_path='/api/v1')
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    app.include_router(user_router, prefix='/user', tags=['User CRUD'])
    app.include_router(
        category_router, prefix='/category', tags=['Category CRUD']
    )
    app.include_router(
        location_router, prefix='/location', tags=['Location CRUD']
    )
    app.include_router(post_router, prefix='/post', tags=['Post CRUD'])
    app.include_router(
        comment_router, prefix='/comment', tags=['Comment CRUD']
    )

    return app
