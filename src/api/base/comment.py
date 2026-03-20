from fastapi import APIRouter, HTTPException, status

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

comment_router = APIRouter()


@comment_router.get('/{id}')
async def get_comment(id: int) -> CommentResponseSchema:
    use_case = GetCommentUseCase()
    try:
        comment = await use_case.execute(id=id)
    except CommentNotFoundByIdException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail()
        )
    return comment


@comment_router.post('/', status_code=status.HTTP_201_CREATED)
async def create_comment(data: CommentRequestSchema) -> CommentResponseSchema:
    use_case = CreateCommentUseCase()
    try:
        comment = await use_case.execute(data=data)
    except (UserNotFoundByIdException, PostNotFoundByIdException) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=e.get_detail()
        )
    return comment


@comment_router.put('/{id}')
async def update_comment(
    id: int, data: CommentRequestSchema
) -> CommentResponseSchema:
    use_case = UpdateCommentUseCase()
    try:
        comment = await use_case.execute(id=id, data=data)
    except CommentNotFoundByIdException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail()
        )
    except (UserNotFoundByIdException, PostNotFoundByIdException) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=e.get_detail()
        )
    return comment


@comment_router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(id: int):
    use_case = DeleteCommentUseCase()
    try:
        comment = await use_case.execute(id=id)
    except CommentNotFoundByIdException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail()
        )
    return comment
