from fastapi import APIRouter, Depends, HTTPException, status

from src.api.depends import (
    create_comment_use_case,
    delete_comment_use_case,
    get_comment_use_case,
    update_comment_use_case,
)
from src.core.exceptions.domain_exceptions import (
    CommentNotFoundByIdException,
    PostNotFoundByIdException,
    UserNotFoundByIdException,
)
from src.domain.comment.use_cases.create_comment import CreateCommentUseCase
from src.domain.comment.use_cases.delete_comment import DeleteCommentUseCase
from src.domain.comment.use_cases.get_comment import GetCommentUseCase
from src.domain.comment.use_cases.update_comment import UpdateCommentUseCase
from src.schemas.comment import CommentResponseSchema, CommentRequestSchema
from src.schemas.user import UserResponseSchema
from src.services.auth import AuthService

router = APIRouter()


@router.get('/{id}', response_model=CommentResponseSchema)
async def get_comment(
    id: int,
    use_case: GetCommentUseCase = Depends(get_comment_use_case),
    current_user: UserResponseSchema | None = Depends(
        AuthService.get_current_user_or_none
    ),
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
async def create_comment(
    data: CommentRequestSchema,
    current_user: UserResponseSchema = Depends(AuthService.get_current_user),
    use_case: CreateCommentUseCase = Depends(create_comment_use_case),
) -> CommentResponseSchema:
    try:
        return await use_case.execute(data=data, current_user=current_user)
    except (UserNotFoundByIdException, PostNotFoundByIdException) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=e.get_detail()
        )


@router.put(
    '/{id}',
    response_model=CommentResponseSchema,
)
async def update_comment(
    id: int,
    data: CommentRequestSchema,
    use_case: UpdateCommentUseCase = Depends(update_comment_use_case),
    current_user: UserResponseSchema = Depends(AuthService.get_current_user),
) -> CommentResponseSchema:
    try:
        return await use_case.execute(
            id=id, data=data, current_user=current_user
        )
    except CommentNotFoundByIdException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail()
        )
    except (UserNotFoundByIdException, PostNotFoundByIdException) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=e.get_detail()
        )


@router.delete(
    '/{id}',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_comment(
    id: int,
    use_case: DeleteCommentUseCase = Depends(delete_comment_use_case),
    current_user: UserResponseSchema = Depends(AuthService.get_current_user),
):
    try:
        return await use_case.execute(id=id, current_user=current_user)
    except CommentNotFoundByIdException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail()
        )
