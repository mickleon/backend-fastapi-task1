import uuid
from fastapi import HTTPException

from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.post import PostRepository
from src.schemas.post import PostRequestSchema, PostResponseSchema


class UpdatePostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(
        self, id: uuid.UUID, data: PostRequestSchema
    ) -> PostResponseSchema:
        with self._database.session() as session:
            post = self._repo.get(session=session, id=id)

            if post is None:
                raise HTTPException(
                    status_code=404, detail=f'Публикация с id "{id}" не найдена'
                )

            self._repo.update(session=session, post=post, data=data)

        return PostResponseSchema.model_validate(obj=post)

