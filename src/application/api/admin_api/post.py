import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status

from application.api.depends import (
    create_post_admin_use_case,
    delete_post_admin_use_case,
    get_post_admin_use_case,
    get_post_comments_admin_use_case,
    update_post_admin_use_case,
)
from application.core.exceptions.domain_exceptions import (
    CategoryNotFoundByIdException,
    ImageNotFoundByIdException,
    LocationNotFoundByIdException,
    PostNotFoundByIdException,
)
from application.domain.post.use_cases.create_post_admin import (
    CreatePostAdminUseCase,
)
from application.domain.post.use_cases.delete_post_admin import (
    DeletePostAdminUseCase,
)
from application.domain.post.use_cases.get_post_admin import GetPostAdminUseCase
from application.domain.post.use_cases.get_post_comments_admin import (
    GetPostCommentsAdminUseCase,
)
from application.domain.post.use_cases.update_post_admin import (
    UpdatePostAdminUseCase,
)
from application.schemas.comment import CommentsPageResponseSchema
from application.schemas.post import (
    PostRequestAdminSchema,
    PostResponseSchema,
    PostUpdateAdminSchema,
)
from application.schemas.user import UserResponseSchema
from application.services.auth import AuthService

router = APIRouter()


@router.get('/{id}', response_model=PostResponseSchema)
async def get_post_admin(
    id: uuid.UUID,
    use_case: GetPostAdminUseCase = Depends(get_post_admin_use_case),
    current_user: UserResponseSchema = Depends(AuthService.require_admin),
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
async def create_post_admin(
    data: PostRequestAdminSchema,
    use_case: CreatePostAdminUseCase = Depends(create_post_admin_use_case),
    current_user: UserResponseSchema = Depends(AuthService.require_admin),
) -> PostResponseSchema:
    try:
        return await use_case.execute(data=data, current_user=current_user)
    except (
        LocationNotFoundByIdException,
        CategoryNotFoundByIdException,
        ImageNotFoundByIdException,
    ) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=e.get_detail()
        )


@router.get('/{id}/comments', response_model=CommentsPageResponseSchema)
async def get_post_comments_admin(
    id: uuid.UUID,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    use_case: GetPostCommentsAdminUseCase = Depends(
        get_post_comments_admin_use_case
    ),
    current_user: UserResponseSchema = Depends(AuthService.require_admin),
) -> CommentsPageResponseSchema:
    try:
        return await use_case.execute(
            id=id,
            page=page,
            page_size=page_size,
            current_user=current_user,
        )
    except PostNotFoundByIdException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail()
        )


@router.put('/{id}', response_model=PostResponseSchema)
async def update_post_admin(
    id: uuid.UUID,
    data: PostUpdateAdminSchema,
    use_case: UpdatePostAdminUseCase = Depends(update_post_admin_use_case),
    current_user: UserResponseSchema = Depends(AuthService.require_admin),
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
        ImageNotFoundByIdException,
    ) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=e.get_detail()
        )


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post_admin(
    id: uuid.UUID,
    use_case: DeletePostAdminUseCase = Depends(delete_post_admin_use_case),
    current_user: UserResponseSchema = Depends(AuthService.require_admin),
):
    try:
        return await use_case.execute(id=id, current_user=current_user)
    except PostNotFoundByIdException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail()
        )
