import uuid
from fastapi import HTTPException

from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.comment import CommentRepository


class DeleteCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, id: uuid.UUID):
        with self._database.session() as session:
            comment = self._repo.get(session=session, id=id)

            if comment is None:
                raise HTTPException(
                    status_code=404, detail=f'Комментарий с id "{id}" не найден'
                )

        self._repo.delete(session=session, comment=comment)

