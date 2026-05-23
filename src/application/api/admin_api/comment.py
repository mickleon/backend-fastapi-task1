import uuid

from fastapi import APIRouter, Depends, HTTPException, status

from application.api.depends import (
    create_comment_admin_use_case,
    delete_comment_admin_use_case,
    get_comment_admin_use_case,
    update_comment_admin_use_case,
)
from application.core.exceptions.domain_exceptions import (
    CommentNotFoundByIdException,
    ImageNotFoundByIdException,
    PostNotFoundByIdException,
)
from application.domain.comment.use_cases.create_comment_admin import (
    CreateCommentAdminUseCase,
)
from application.domain.comment.use_cases.delete_comment_admin import (
    DeleteCommentAdminUseCase,
)
from application.domain.comment.use_cases.get_comment_admin import (
    GetCommentAdminUseCase,
)
from application.domain.comment.use_cases.update_comment_admin import (
    UpdateCommentAdminUseCase,
)
from application.schemas.comment import (
    CommentRequestAdminSchema,
    CommentResponseSchema,
)
from application.schemas.user import UserResponseSchema
from application.services.auth import AuthService

router = APIRouter()


@router.get('/{id}', response_model=CommentResponseSchema)
async def get_comment_admin(
    id: uuid.UUID,
    use_case: GetCommentAdminUseCase = Depends(get_comment_admin_use_case),
    current_user: UserResponseSchema = Depends(AuthService.require_admin),
) -> CommentResponseSchema:
    try:
        return await use_case.execute(id=id, current_user=current_user)
    except CommentNotFoundByIdException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail()
        )


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=CommentResponseSchema,
)
async def create_comment_admin(
    data: CommentRequestAdminSchema,
    current_user: UserResponseSchema = Depends(AuthService.require_admin),
    use_case: CreateCommentAdminUseCase = Depends(
        create_comment_admin_use_case
    ),
) -> CommentResponseSchema:
    try:
        return await use_case.execute(data=data, current_user=current_user)
    except (PostNotFoundByIdException, ImageNotFoundByIdException) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=e.get_detail()
        )


@router.put('/{id}', response_model=CommentResponseSchema)
async def update_comment_admin(
    id: uuid.UUID,
    data: CommentRequestAdminSchema,
    use_case: UpdateCommentAdminUseCase = Depends(
        update_comment_admin_use_case
    ),
    current_user: UserResponseSchema = Depends(AuthService.require_admin),
) -> CommentResponseSchema:
    try:
        return await use_case.execute(
            id=id, data=data, current_user=current_user
        )
    except CommentNotFoundByIdException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail()
        )
    except ImageNotFoundByIdException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=e.get_detail()
        )


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment_admin(
    id: uuid.UUID,
    use_case: DeleteCommentAdminUseCase = Depends(
        delete_comment_admin_use_case
    ),
    current_user: UserResponseSchema = Depends(AuthService.require_admin),
):
    try:
        return await use_case.execute(id=id, current_user=current_user)
    except CommentNotFoundByIdException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail()
        )
