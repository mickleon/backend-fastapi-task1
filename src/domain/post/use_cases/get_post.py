import uuid

from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.post import PostRepository
from src.schemas.post import PostResponseSchema


class GetPostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(self, id: uuid.UUID) -> PostResponseSchema:
        with self._database.session() as session:
            post = self._repo.get(session=session, id=id)

            return PostResponseSchema.model_validate(obj=post)

