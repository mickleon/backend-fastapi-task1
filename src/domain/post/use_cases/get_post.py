import uuid

from src.core.exceptions.database_exceptions import PostNotFoundException
from src.core.exceptions.domain_exceptions import PostNotFoundByIdException
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.post import PostRepository
from src.schemas.post import PostResponseSchema


class GetPostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(self, id: uuid.UUID) -> PostResponseSchema:
        with self._database.session() as session:
            try:
                post = self._repo.get(session=session, id=id)
            except PostNotFoundException:
                raise PostNotFoundByIdException(id=id)

            return PostResponseSchema.model_validate(obj=post)
