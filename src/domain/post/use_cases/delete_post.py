import uuid
from fastapi import HTTPException

from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.post import PostRepository


class DeletePostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(self, id: uuid.UUID):
        with self._database.session() as session:
            post = self._repo.get(session=session, id=id)

            if post is None:
                raise HTTPException(
                    status_code=404, detail=f'Публикация с id "{id}" не найдена'
                )

        self._repo.delete(session=session, post=post)

