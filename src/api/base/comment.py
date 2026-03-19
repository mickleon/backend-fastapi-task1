from fastapi import APIRouter
from starlette import status

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
    return await use_case.execute(id=id)


@comment_router.post('/', status_code=status.HTTP_201_CREATED)
async def create_comment(data: CommentRequestSchema) -> CommentResponseSchema:
    use_case = CreateCommentUseCase()
    return await use_case.execute(data=data)


@comment_router.put('/{id}')
async def update_comment(
    id: int, data: CommentRequestSchema
) -> CommentResponseSchema:
    use_case = UpdateCommentUseCase()
    return await use_case.execute(id=id, data=data)


@comment_router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(id: int):
    use_case = DeleteCommentUseCase()
    await use_case.execute(id)
    return {'message': f'Комментарий с id "{id}" успешно удален'}

