import uuid

from fastapi import APIRouter, Depends, HTTPException, status

from application.api.depends import (
    create_post_use_case,
    delete_post_use_case,
    get_post_use_case,
    update_post_use_case,
)
from application.core.exceptions.domain_exceptions import (
    CategoryNotFoundByIdException,
    LocationNotFoundByIdException,
    PostNotFoundByIdException,
)
from application.domain.post.use_cases.create_post import CreatePostUseCase
from application.domain.post.use_cases.delete_post import DeletePostUseCase
from application.domain.post.use_cases.get_post import GetPostUseCase
from application.domain.post.use_cases.update_post import UpdatePostUseCase
from application.schemas.post import PostRequestSchema, PostResponseSchema
from application.schemas.user import UserResponseSchema
from application.services.auth import AuthService

router = APIRouter()


@router.get('/{id}', response_model=PostResponseSchema)
async def get_post(
    id: uuid.UUID,
    use_case: GetPostUseCase = Depends(get_post_use_case),
    current_user: UserResponseSchema | None = Depends(
        AuthService.get_current_user_or_none
    ),
) -> PostResponseSchema:
    try:
        return await use_case.execute(id=id, current_user=current_user)
    except PostNotFoundByIdException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail()
        )


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=PostResponseSchema,
)
async def create_post(
    data: PostRequestSchema,
    use_case: CreatePostUseCase = Depends(create_post_use_case),
    current_user: UserResponseSchema = Depends(AuthService.get_current_user),
) -> PostResponseSchema:
    try:
        return await use_case.execute(data=data, current_user=current_user)
    except (
        LocationNotFoundByIdException,
        CategoryNotFoundByIdException,
    ) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=e.get_detail()
        )


@router.put(
    '/{id}',
    response_model=PostResponseSchema,
)
async def update_post(
    id: uuid.UUID,
    data: PostRequestSchema,
    use_case: UpdatePostUseCase = Depends(update_post_use_case),
    current_user: UserResponseSchema = Depends(AuthService.get_current_user),
) -> PostResponseSchema:
    try:
        return await use_case.execute(
            id=id, data=data, current_user=current_user
        )
    except PostNotFoundByIdException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail()
        )
    except (
        LocationNotFoundByIdException,
        CategoryNotFoundByIdException,
    ) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=e.get_detail()
        )


@router.delete(
    '/{id}',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_post(
    id: uuid.UUID,
    use_case: DeletePostUseCase = Depends(delete_post_use_case),
    current_user: UserResponseSchema = Depends(AuthService.get_current_user),
):
    try:
        return await use_case.execute(id=id, current_user=current_user)
    except PostNotFoundByIdException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail()
        )
