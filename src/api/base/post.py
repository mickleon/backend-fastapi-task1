import uuid
from fastapi import APIRouter

from src.domain.post.use_cases.create_post import CreatePostUseCase
from src.domain.post.use_cases.delete_post import (
    DeletePostUseCase,
)
from src.domain.post.use_cases.get_post import (
    GetPostUseCase,
)
from src.domain.post.use_cases.update_post import (
    UpdatePostUseCase,
)
from src.schemas.post import PostResponseSchema, PostRequestSchema

post_router = APIRouter()


@post_router.get('/{id}')
async def get_post(id: uuid.UUID) -> PostResponseSchema:
    use_case = GetPostUseCase()
    return await use_case.execute(id=id)


@post_router.post('/')
async def create_post(data: PostRequestSchema) -> PostResponseSchema:
    use_case = CreatePostUseCase()
    return await use_case.execute(data=data)


@post_router.put('/{id}')
async def update_post(id: uuid.UUID, data: PostRequestSchema) -> PostResponseSchema:
    use_case = UpdatePostUseCase()
    return await use_case.execute(id=id, data=data)


@post_router.delete('/{id}')
async def delete_post(id: uuid.UUID):
    use_case = DeletePostUseCase()
    await use_case.execute(id)
    return {'message': f'Публикация с id "{id}" успешно удаленa'}

