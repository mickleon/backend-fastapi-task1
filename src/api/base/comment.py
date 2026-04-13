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
from src.domain.comment.use_cases.delete_comment import (
    DeleteCommentUseCase,
)
from src.domain.comment.use_cases.get_comment import (
    GetCommentUseCase,
)
from src.domain.comment.use_cases.update_comment import (
    UpdateCommentUseCase,
)
from src.schemas.comment import CommentResponseSchema, CommentRequestSchema

router = APIRouter()


@router.get('/{id}', response_model=CommentResponseSchema)
async def get_comment(
    id: int,
    use_case: GetCommentUseCase = Depends(get_comment_use_case),
) -> CommentResponseSchema:
    try:
        return await use_case.execute(id=id)
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
    use_case: CreateCommentUseCase = Depends(create_comment_use_case),
) -> CommentResponseSchema:
    try:
        return await use_case.execute(data=data)
    except (UserNotFoundByIdException, PostNotFoundByIdException) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=e.get_detail()
        )


@router.put('/{id}', response_model=CommentResponseSchema)
async def update_comment(
    id: int,
    data: CommentRequestSchema,
    use_case: UpdateCommentUseCase = Depends(update_comment_use_case),
) -> CommentResponseSchema:
    try:
        return await use_case.execute(id=id, data=data)
    except CommentNotFoundByIdException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail()
        )
    except (UserNotFoundByIdException, PostNotFoundByIdException) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=e.get_detail()
        )


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    id: int,
    use_case: DeleteCommentUseCase = Depends(delete_comment_use_case),
):
    try:
        return await use_case.execute(id=id)
    except CommentNotFoundByIdException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail()
        )
