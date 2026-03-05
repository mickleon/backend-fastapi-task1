import uuid
from fastapi import HTTPException

from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.comment import CommentRepository
from src.schemas.comment import CommentRequestSchema, CommentResponseSchema


class UpdateCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(
        self, id: uuid.UUID, data: CommentRequestSchema
    ) -> CommentResponseSchema:
        with self._database.session() as session:
            comment = self._repo.get(session=session, id=id)

            if comment is None:
                raise HTTPException(
                    status_code=404, detail=f'Комментарий с id "{id}" не найден'
                )

            self._repo.update(session=session, comment=comment, data=data)

        return CommentResponseSchema.model_validate(obj=comment)

