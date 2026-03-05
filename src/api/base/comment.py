import uuid
from fastapi import APIRouter

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
async def get_comment(id: uuid.UUID) -> CommentResponseSchema:
    use_case = GetCommentUseCase()
    return await use_case.execute(id=id)


@comment_router.post('/')
async def create_comment(data: CommentRequestSchema) -> CommentResponseSchema:
    use_case = CreateCommentUseCase()
    return await use_case.execute(data=data)


@comment_router.put('/{id}')
async def update_comment(
    id: uuid.UUID, data: CommentRequestSchema
) -> CommentResponseSchema:
    use_case = UpdateCommentUseCase()
    return await use_case.execute(id=id, data=data)


@comment_router.delete('/{id}')
async def delete_comment(id: uuid.UUID):
    use_case = DeleteCommentUseCase()
    await use_case.execute(id)
    return {'message': f'Комментарий с id "{id}" успешно удален'}

