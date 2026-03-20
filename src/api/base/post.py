import uuid
from fastapi import APIRouter, HTTPException, status

from src.core.exceptions.domain_exceptions import (
    CategoryNotFoundByIdException,
    LocationNotFoundByIdException,
    PostNotFoundByIdException,
    UserNotFoundByIdException,
)
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
    try:
        post = await use_case.execute(id=id)
    except PostNotFoundByIdException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail()
        )
    return post


@post_router.post('/', status_code=status.HTTP_201_CREATED)
async def create_post(data: PostRequestSchema) -> PostResponseSchema:
    use_case = CreatePostUseCase()
    try:
        post = await use_case.execute(data=data)
    except (
        UserNotFoundByIdException,
        LocationNotFoundByIdException,
        CategoryNotFoundByIdException,
    ) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=e.get_detail()
        )
    return post


@post_router.put('/{id}')
async def update_post(
    id: uuid.UUID, data: PostRequestSchema
) -> PostResponseSchema:
    use_case = UpdatePostUseCase()
    try:
        post = await use_case.execute(id=id, data=data)
    except PostNotFoundByIdException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail()
        )
    except (
        UserNotFoundByIdException,
        LocationNotFoundByIdException,
        CategoryNotFoundByIdException,
    ) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=e.get_detail()
        )
    return post


@post_router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: uuid.UUID):
    use_case = DeletePostUseCase()
    try:
        post = await use_case.execute(id=id)
    except PostNotFoundByIdException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail()
        )
    return post
