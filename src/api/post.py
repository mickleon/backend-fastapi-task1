import uuid
from fastapi import APIRouter, Depends, HTTPException, status

from src.api.depends import (
    create_post_use_case,
    delete_post_use_case,
    get_post_use_case,
    update_post_use_case,
)
from src.core.exceptions.domain_exceptions import (
    CategoryNotFoundByIdException,
    LocationNotFoundByIdException,
    PostNotFoundByIdException,
    UserNotFoundByIdException,
)
from src.domain.post.use_cases.create_post import CreatePostUseCase
from src.domain.post.use_cases.delete_post import DeletePostUseCase
from src.domain.post.use_cases.get_post import GetPostUseCase
from src.domain.post.use_cases.update_post import UpdatePostUseCase
from src.schemas.post import PostResponseSchema, PostRequestSchema
from src.services.auth import AuthService

router = APIRouter()


@router.get('/{id}', response_model=PostResponseSchema)
async def get_post(
    id: uuid.UUID,
    use_case: GetPostUseCase = Depends(get_post_use_case),
) -> PostResponseSchema:
    try:
        return await use_case.execute(id=id)
    except PostNotFoundByIdException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail()
        )


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=PostResponseSchema,
    dependencies=[Depends(AuthService.get_current_user)],
)
async def create_post(
    data: PostRequestSchema,
    use_case: CreatePostUseCase = Depends(create_post_use_case),
) -> PostResponseSchema:
    try:
        return await use_case.execute(data=data)
    except (
        UserNotFoundByIdException,
        LocationNotFoundByIdException,
        CategoryNotFoundByIdException,
    ) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=e.get_detail()
        )


@router.put(
    '/{id}',
    response_model=PostResponseSchema,
    dependencies=[Depends(AuthService.get_current_user)],
)
async def update_post(
    id: uuid.UUID,
    data: PostRequestSchema,
    use_case: UpdatePostUseCase = Depends(update_post_use_case),
) -> PostResponseSchema:
    try:
        return await use_case.execute(id=id, data=data)
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


@router.delete(
    '/{id}',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(AuthService.get_current_user)],
)
async def delete_post(
    id: uuid.UUID,
    use_case: DeletePostUseCase = Depends(delete_post_use_case),
):
    try:
        return await use_case.execute(id=id)
    except PostNotFoundByIdException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail()
        )
